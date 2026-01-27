from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from user_permission.models import User, UserRole, Role, Department
from user_permission.serializers.user_serializers import UserUpdateCreateSerializer, UserListSerializer
from user_permission.utils.image_utils import save_avatar_file
from utils.decorators import atomic_view
from utils.serializer_errors import extract_error_message
from utils.validators import strict_validate_fields
from user_permission.signals.permission_signals import permissions_changed


class UserListAPIView(APIView):
    """用户列表和创建"""

    def get(self, request):
        """获取用户列表 - 使用 UserListSerializer"""
        try:
            # 获取查询参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            username = request.GET.get('username', '').strip()
            user_id = request.GET.get('id', '').strip()
            real_name = request.GET.get('real_name', '').strip()
            phone = request.GET.get('phone', '').strip()
            status_param = request.GET.get('status', '').strip()
            create_time_start = request.GET.get('create_time_start', '').strip()
            create_time_end = request.GET.get('create_time_end', '').strip()

            # 构建查询条件
            queryset = User.objects.filter(is_deleted=0)

            if username:
                queryset = queryset.filter(username__icontains=username)

            if user_id:
                queryset = queryset.filter(id=user_id)

            if real_name:
                queryset = queryset.filter(real_name__icontains=real_name)

            if phone:
                queryset = queryset.filter(phone__icontains=phone)

            if status_param:
                queryset = queryset.filter(status=int(status_param))

            if create_time_start and create_time_end:
                queryset = queryset.filter(
                    create_time__gte=create_time_start,
                    create_time__lte=create_time_end
                )

            # 排序
            queryset = queryset.order_by('-create_time')

            # 分页前优化查询
            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)

            # 使用序列化器的优化方法
            optimized_queryset = UserListSerializer.setup_eager_loading(page_obj.object_list)

            # 序列化数据 - 使用 UserListSerializer
            serializer = UserListSerializer(optimized_queryset, many=True, context={'request': request})

            response_data = {
                'success': True,
                'data': {
                    'count': paginator.count,
                    'results': serializer.data,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': paginator.num_pages
                },
                'message': '获取用户列表成功'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'获取用户列表失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @atomic_view
    def post(self, request):
        """创建用户"""
        user_schema = {
            "avatar": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "department_id": {"type": (int, type(None)), "required": False},
            "email": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "password": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "phone": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "real_name": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "status": {
                "type": int,
                "required": True,
                "choices": [0, 1]
            },
            "role_ids": {
                "type": list,
                "required": False
            },
            "username": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
        }

        error_response = strict_validate_fields(request.data, user_schema)
        if error_response:
            return error_response
        try:
            data = request.data.copy()

            # 提前处理头像数据流
            avatar_data = data.get('avatar', '')
            if avatar_data.startswith('data:image'):
                filename = save_avatar_file(avatar_data)
                data['avatar'] = filename if filename else None

            # 创建序列化器
            serializer = UserUpdateCreateSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                user = serializer.save()
                user_data = UserListSerializer(user, context={'request': request}).data
                return Response({
                    'success': True,
                    'data': user_data,
                    'message': '用户创建成功'
                }, status=status.HTTP_201_CREATED)
            else:
                message = extract_error_message(serializer.errors)
                return Response({
                    'success': False,
                    'message': message,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'创建用户失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailAPIView(APIView):
    """用户详情、更新、启用/禁用"""

    def get(self, request, pk):
        """获取用户详情"""
        try:
            user = User.objects.get(id=pk, is_deleted=0)

            # 预加载角色信息
            roles = UserRole.objects.filter(user_id=user.id)
            role_ids = [r.role_id for r in roles]
            user._roles = [
                {'id': role.id, 'name': role.name, 'code': role.code}
                for role in Role.objects.filter(id__in=role_ids)
            ]

            # 预加载部门和创建人信息（复用列表序列化器逻辑）
            if user.department_id:
                dept = Department.objects.filter(id=user.department_id).first()
                user._department_name = dept.name if dept else None
            if user.creator_id:
                creator = User.objects.filter(id=user.creator_id).first()
                user._creator_name = creator.username if creator else None

            serializer = UserListSerializer(user, context={'request': request})
            return Response({
                'success': True,
                'data': serializer.data,
                'message': '获取用户详情成功'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'获取用户详情失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @atomic_view
    def post(self, request, pk):

        """更新用户信息或启用/禁用用户"""
        user_schema = {
            "avatar": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "department_id": {"type": (int, type(None)), "required": False},
            "email": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "phone": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "real_name": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "status": {
                "type": int,
                "required": True,
                "choices": [0, 1]
            },
            "role_ids": {
                "type": list,
                "required": False
            },
            "username": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "action": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
        }

        error_response = strict_validate_fields(request.data, user_schema)
        if error_response:
            return error_response
        try:
            action = request.data.get('action')
            user = User.objects.get(id=pk, is_deleted=0)

            if action == 'enable':
                user.status = 1
                user.save()
                return Response({
                    'success': True,
                    'message': '用户启用成功'
                }, status=status.HTTP_200_OK)

            elif action == 'disable':
                user.status = 0
                user.save()
                return Response({
                    'success': True,
                    'message': '用户禁用成功'
                }, status=status.HTTP_200_OK)


            elif action == 'update':
                # 提前处理头像数据流
                data = request.data.copy()
                avatar_data = data.get('avatar', '')
                if avatar_data.startswith('data:image'):
                    filename = save_avatar_file(avatar_data)
                    data['avatar'] = filename if filename else None
                elif avatar_data.startswith('/avatars'):
                    data['avatar'] = avatar_data.strip("/avatars/")

                # 更新用户信息
                serializer = UserUpdateCreateSerializer(user, data=data, partial=True, context={'request': request})
                if serializer.is_valid():
                    updated_user = serializer.save()

                    # ✅ 更新角色信息（如果传了 role_ids）
                    role_ids = data.get('role_ids')
                    if role_ids is not None:
                        # 清除旧角色
                        UserRole.objects.filter(user_id=user.id).delete()
                        # 添加新角色
                        creator_id = request.user.id if hasattr(request, 'user') else None
                        new_roles = [
                            UserRole(user_id=user.id, role_id=rid, creator_id=creator_id)
                            for rid in role_ids
                        ]
                        UserRole.objects.bulk_create(new_roles)

                        # 🔥 自动刷新权限缓存（信号机制）
                        permissions_changed.send(sender=None, user_ids=[user.id])

                    # 返回更新后的数据
                    user_data = UserListSerializer(updated_user, context={'request': request}).data
                    return Response({
                        'success': True,
                        'message': '用户更新成功',
                        'data': user_data
                    }, status=status.HTTP_200_OK)
                else:
                    message = extract_error_message(serializer.errors)
                    return Response({
                        'success': False,
                        'message': message,
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'message': '未知操作'
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'操作失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDeleteAPIView(APIView):
    """删除用户（软删除）并清除角色关联"""

    @atomic_view
    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk, is_deleted=0)

            # 软删除用户
            user.is_deleted = 1
            user.save()

            # 删除用户角色关联
            UserRole.objects.filter(user_id=user.id).delete()

            return Response({
                'success': True,
                'message': '用户及角色关联删除成功'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'删除用户失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

