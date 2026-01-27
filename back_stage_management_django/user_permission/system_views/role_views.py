from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from user_permission.models import Role, RolePermission,UserRole
from user_permission.serializers.role_serializers import RoleSerializer, RoleUpdateCreateSerializer
from utils.decorators import atomic_view
from utils.serializer_errors import extract_error_message
from utils.validators import strict_validate_fields
from user_permission.signals.permission_signals import permissions_changed



class RoleListCreateView(APIView):
    """
    角色列表和创建视图
    """

    def get(self, request):
        """获取角色列表"""
        try:
            # 获取分页参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 20))

            # 构建查询条件
            queryset = Role.objects.filter(is_deleted=0)

            # 检查是否有搜索参数
            has_search_params = False
            search_params = {}

            # 获取搜索参数
            name = request.GET.get('name', '')
            id_filter = request.GET.get('id', '')
            status_filter = request.GET.get('status', '')
            create_time_start = request.GET.get('create_time_start', '')
            create_time_end = request.GET.get('create_time_end', '')

            # 应用搜索条件
            if name:
                queryset = queryset.filter(name__icontains=name)
                search_params['name'] = name
                has_search_params = True

            if id_filter:
                queryset = queryset.filter(id=int(id_filter))
                search_params['id'] = id_filter
                has_search_params = True

            if status_filter:
                queryset = queryset.filter(status=int(status_filter))
                search_params['status'] = status_filter
                has_search_params = True

            if create_time_start and create_time_end:
                queryset = queryset.filter(
                    create_time__date__gte=create_time_start,
                    create_time__date__lte=create_time_end
                )
                search_params['create_time_start'] = create_time_start
                search_params['create_time_end'] = create_time_end
                has_search_params = True

            # 如果没有搜索参数，使用默认排序（按创建时间倒序）
            if not has_search_params:
                queryset = queryset.order_by('-create_time')
            else:
                # 如果有搜索参数，可以按相关度或其他逻辑排序
                queryset = queryset.order_by('-create_time')

            # 分页
            paginator = Paginator(queryset, page_size)
            try:
                roles = paginator.page(page)
            except:
                roles = paginator.page(1)

            serializer = RoleSerializer(roles, many=True)

            response_data = {
                'success': True,
                'data': {
                    'count': paginator.count,
                    'total_pages': paginator.num_pages,
                    'current_page': page,
                    'results': serializer.data,
                    'has_search': has_search_params,
                    'search_params': search_params if has_search_params else None
                }
            }

            return Response(response_data)

        except ValueError as e:
            return Response({
                'success': False,
                'message': f'参数格式错误: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'获取角色列表失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @atomic_view
    def post(self, request):
        """创建角色"""
        # ✅ 前置字段完整性校验
        # 定义角色创建字段验证规则
        role_schema = {
            "name": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "code": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "description": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "status": {
                "type": int,
                "required": True,
                "choices": [0, 1]
            },
            "permissions": {
                "type": list,
                "required": False
            }
        }

        error_response = strict_validate_fields(request.data, role_schema)
        if error_response:
            return error_response
        serializer = RoleUpdateCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 设置创建人
            role = serializer.save(creator_id=request.my_user.id)
            # 获取权限 ID 列表
            permission_ids = request.data.get("permissions", [])
            if isinstance(permission_ids, list) and permission_ids:
                role_permissions = [
                    RolePermission(
                        role_id=role.id,
                        permission_id=pid,
                        creator_id=request.my_user.id
                    )
                    for pid in permission_ids
                ]
                RolePermission.objects.bulk_create(role_permissions)

            return Response({
                'success': True,
                'message': '角色创建成功',
                'data': RoleSerializer(role).data
            }, status=status.HTTP_201_CREATED)
        message = extract_error_message(serializer.errors)
        return Response({
            'success': False,
            'message': message,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RoleDetailView(APIView):
    """
    角色详情、更新视图
    """

    def get_object(self, pk):
        """获取角色对象"""
        try:
            return Role.objects.get(id=pk, is_deleted=0)
        except Role.DoesNotExist:
            return None

    def get(self, request, pk):
        """获取角色详情"""
        role = self.get_object(pk)
        if not role:
            return Response({
                'success': False,
                'message': '角色不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role)

        # 查询权限 ID 列表
        permission_ids = RolePermission.objects.filter(
            role_id=pk
        ).values_list('permission_id', flat=True)

        # 合并数据
        data = serializer.data
        data['permissions'] = list(permission_ids)

        return Response({
            'success': True,
            'data': data
        })

    @atomic_view
    def post(self, request, pk):
        """更新或删除角色"""

        role_schema = {
            "action": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "name": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "code": {
                "type": str,
                "required": True,
                "allow_blank": False
            },
            "description": {
                "type": str,
                "required": False,
                "allow_blank": True
            },
            "status": {
                "type": int,
                "required": True,
                "choices": [0, 1]
            },
            "permissions": {
                "type": list,
                "required": False
            }
        }

        error_response = strict_validate_fields(request.data, role_schema)
        if error_response:
            return error_response

        role = self.get_object(pk)
        if not role:
            return Response({
                'success': False,
                'message': '角色不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action', '')

        if action == 'update':
            # 检查是否要更新状态为禁用，并且有用户使用
            new_status = request.data.get('status')
            if new_status == 0 and role.status != 0:  # 状态从启用变为禁用
                using_users_count = role.get_using_users_count()
                if using_users_count > 0:
                    return Response({
                        'success': False,
                        'message': f'无法禁用角色，当前有 {using_users_count} 个用户正在使用此角色'
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer = RoleUpdateCreateSerializer(role, data=request.data, partial=True)
            if serializer.is_valid():

                serializer.save()

                # 更新权限绑定
                permission_ids = request.data.get("permissions", [])
                if isinstance(permission_ids, list):
                    # 删除旧权限
                    RolePermission.objects.filter(role_id=role.id).delete()

                    # 添加新权限
                    new_permissions = [
                        RolePermission(
                            role_id=role.id,
                            permission_id=pid,
                            creator_id=request.user.id
                        )
                        for pid in permission_ids
                    ]
                    RolePermission.objects.bulk_create(new_permissions)

                # 🔥 找到所有使用该角色的用户
                user_ids = list( UserRole.objects.filter(role_id=role.id).values_list("user_id", flat=True) )
                # 🔥 触发权限刷新信号（自动删除缓存）
                permissions_changed.send(sender=None, user_ids=user_ids)

                return Response({
                    'success': True,
                    'message': '角色更新成功',
                    'data': RoleSerializer(role).data
                })
            message = extract_error_message(serializer.errors)
            return Response({
                'success': False,
                'message': message,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'enable':
            # 启用角色
            role.status = 1
            role.save()
            return Response({
                'success': True,
                'message': '角色已启用'
            })

        elif action == 'disable':
            # 禁用角色前检查是否有用户使用
            using_users_count = role.get_using_users_count()
            if using_users_count > 0:
                return Response({
                    'success': False,
                    'message': f'无法禁用角色，当前有 {using_users_count} 个用户正在使用此角色'
                }, status=status.HTTP_400_BAD_REQUEST)
            # 禁用角色
            role.status = 0
            role.save()
            return Response({
                'success': True,
                'message': '角色已禁用'
            })

        else:
            return Response({
                'success': False,
                'message': '未知操作'
            }, status=status.HTTP_400_BAD_REQUEST)


class RoleDeleteView(APIView):
    """
        角色删除视图
        """

    def get_object(self, pk):
        """获取角色对象"""
        try:
            return Role.objects.get(id=pk, is_deleted=0)
        except Role.DoesNotExist:
            return None

    @atomic_view
    def post(self, request, pk):
        role = self.get_object(pk)
        if not role:
            return Response({
                'success': False,
                'message': '角色不存在'
            }, status=status.HTTP_404_NOT_FOUND)

            # 删除前检查是否有用户使用
        using_users_count = role.get_using_users_count()
        if using_users_count > 0:
            return Response({
                'success': False,
                'message': f'无法删除角色，当前有 {using_users_count} 个用户正在使用此角色'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 软删除角色
        role.is_deleted = 1
        role.save()
        # 删除角色关联的权限
        RolePermission.objects.filter(role_id=role.id).delete()
        return Response({
            'success': True,
            'message': '角色删除成功'
        })




