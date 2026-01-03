from user_permission.models import RolePermission, Permission,UserRole
from user_permission.serializers.permission_serializers import PermissionSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.serializer_errors import extract_error_message
from utils.decorators import atomic_view
from utils.validators import strict_validate_fields
from user_permission.signals.permission_signals import permissions_changed


def get_permission_schema(data=None, is_update=False):
    """
    根据权限类型动态生成验证规则
    """
    if data:
        permission_type = data.get('type')
    else:
        permission_type = None

    # 基础规则（所有权限类型通用）
    base_schema = {
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
        "type": {
            "type": int,
            "required": True,
            "choices": [1, 2, 3]
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
        }
    }

    if not is_update:
        base_schema["parent_id"] = {
            "type": int,
            "required": False,
            "allow_blank": True
        }

    # 根据权限类型添加特定字段
    if permission_type is not None:
        if int(permission_type) == 1:  # 菜单权限
            base_schema["menu_id"] = {
                "type": int,
                "required": True,
                "allow_blank": False
            }
        elif int(permission_type) == 2:  # 接口权限
            base_schema["api_method"] = {
                "type": str,
                "required": True,
                "allow_blank": False
            }
            base_schema["api_path"] = {
                "type": str,
                "required": True,
                "allow_blank": False
            }

    return base_schema


class PermissionListView(APIView):
    def get(self, request):
        permissions = Permission.objects.filter(is_deleted=0).order_by('create_time')
        data = self.build_tree(permissions)
        return Response({"data": data})

    def build_tree(self, queryset):
        permission_map = {perm.id: PermissionSerializer(perm).data for perm in queryset}
        tree = []

        for perm in permission_map.values():
            pid = perm['parent_id']
            if pid and pid in permission_map:
                parent = permission_map[pid]
                parent.setdefault('children', []).append(perm)
            else:
                tree.append(perm)

        def sort_children(nodes):
            for node in nodes:
                if 'children' in node:
                    node['children'].sort(key=lambda x: x.get('create_time', ''))
                    sort_children(node['children'])

        sort_children(tree)
        return tree


class PermissionCreateView(APIView):
    @atomic_view
    def post(self, request):
        """创建权限"""
        data = request.data

        schema = get_permission_schema(data=data, is_update=False)
        error_response = strict_validate_fields(data, schema)
        if error_response:
            return error_response

        serializer = PermissionSerializer(data=request.data)
        if not serializer.is_valid():
            message = extract_error_message(serializer.errors)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        permission = serializer.save(creator_id=request.my_user.id if request.my_user else None)

        # 自动分配给管理员角色
        RolePermission.objects.get_or_create(
            role_id=1,
            permission_id=permission.id,
            defaults={"creator_id": request.my_user.id if request.my_user else None}
        )

        # 找到管理员角色下所有用户
        admin_user_ids = list(
            UserRole.objects.filter(role_id=1).values_list("user_id", flat=True)
        )

        # 触发信号
        permissions_changed.send(sender=None, user_ids=admin_user_ids)

        return Response({
            "message": "权限创建成功，已自动分配给管理员角色",
            "permission_id": permission.id,
            "code": permission.code
        }, status=status.HTTP_201_CREATED)


class PermissionUpdateView(APIView):
    @atomic_view
    def post(self, request, pk):
        """更新权限"""
        data = request.data

        schema = get_permission_schema(data=data, is_update=True)
        error_response = strict_validate_fields(data, schema)
        if error_response:
            return error_response

        try:
            permission = Permission.objects.get(id=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionSerializer(permission, data=request.data, partial=True)
        if not serializer.is_valid():
            message = extract_error_message(serializer.errors)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(update_time=timezone.now())

        # ⭐ 找出所有拥有该权限的角色
        role_ids = RolePermission.objects.filter(permission_id=pk).values_list("role_id", flat=True)

        # ⭐ 找出所有使用这些角色的用户
        user_ids = list( UserRole.objects.filter(role_id__in=role_ids).values_list("user_id", flat=True) )
        # ⭐ 触发信号（自动刷新缓存）
        permissions_changed.send(sender=None, user_ids=user_ids)

        return Response({"message": "权限更新成功"})


class PermissionDeleteView(APIView):
    @atomic_view
    def post(self, request, pk):
        try:
            root = Permission.objects.get(pk=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)

        def get_descendants(permission):
            children = Permission.objects.filter(parent_id=permission.id, is_deleted=0)
            descendants = list(children)
            for child in children:
                descendants.extend(get_descendants(child))
            return descendants

        all_permissions = [root] + get_descendants(root)
        ids = [p.id for p in all_permissions]

        # ⭐ 找出所有拥有这些权限的角色
        role_ids = RolePermission.objects.filter(permission_id__in=ids).values_list("role_id", flat=True)

        # ⭐ 找出所有拥有这些权限的角色
        role_ids = RolePermission.objects.filter(permission_id__in=ids).values_list("role_id", flat=True)
        # ⭐ 找出所有使用这些角色的用户
        user_ids = list( UserRole.objects.filter(role_id__in=role_ids).values_list("user_id", flat=True) )

        # 逻辑删除权限
        Permission.objects.filter(id__in=ids).update(is_deleted=1, update_time=timezone.now())

        # 删除角色权限关联
        RolePermission.objects.filter(permission_id__in=ids).delete()

        # ⭐ 触发信号（自动刷新缓存）
        permissions_changed.send(sender=None, user_ids=user_ids)

        return Response({"message": "权限及其子权限已删除，角色关联已清理"})
