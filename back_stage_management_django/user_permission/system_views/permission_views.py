from user_permission.models import Department, Role, User, UserRole, RolePermission, Permission, Menu
from user_permission.serializers.permission_serializers import PermissionSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.serializer_errors import extract_error_message
from utils.decorators import atomic_view
from utils.validators import strict_validate_fields


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
    if int(permission_type) == 1:  # 菜单权限
        print(">>>>>>>>>1")
        base_schema["menu_id"] = {
            "type": int,
            "required": True,
            "allow_blank": False
        }
    elif int(permission_type) == 2:  # 接口权限
        print(">>>>>>>>>>>>>>>>>>>>2>")
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
        # ✅ 按创建时间排序（你可以改成其他字段，比如 name 或 status）
        permissions = Permission.objects.filter(is_deleted=0).order_by('create_time')
        data = self.build_tree(permissions)
        return Response({"data": data})

    def build_tree(self, queryset):
        # ✅ 构建权限映射
        permission_map = {perm.id: PermissionSerializer(perm).data for perm in queryset}
        tree = []

        # ✅ 构建树结构
        for perm in permission_map.values():
            pid = perm['parent_id']
            if pid and pid in permission_map:
                parent = permission_map[pid]
                parent.setdefault('children', []).append(perm)
            else:
                tree.append(perm)

        # ✅ 对每个 children 列表按创建时间排序（你也可以改成其他字段）
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

        # ✅ 动态获取验证规则
        schema = get_permission_schema(data=data, is_update=False)

        # ✅ 使用原来的 strict_validate_fields 函数
        error_response = strict_validate_fields(data, schema)
        if error_response:
            return error_response

        serializer = PermissionSerializer(data=request.data)
        if not serializer.is_valid():
            message = extract_error_message(serializer.errors)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 保存权限
        permission = serializer.save(creator_id=request.my_user.id if request.my_user else None)

        # ✅ 创建角色权限关联（避免重复）
        RolePermission.objects.get_or_create(
            role_id=1,
            permission_id=permission.id,
            defaults={"creator_id": request.my_user.id if request.my_user else None}
        )

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

        # ✅ 动态获取验证规则（更新时所有字段都是可选的）
        schema = get_permission_schema(data=data, is_update=True)

        # ✅ 使用原来的 strict_validate_fields 函数
        error_response = strict_validate_fields(data, schema)
        if error_response:
            return error_response

        try:
            permission = Permission.objects.get(id=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ 使用序列化器进行完整验证
        serializer = PermissionSerializer(permission, data=request.data, partial=True)
        if not serializer.is_valid():
            message = extract_error_message(serializer.errors)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save(update_time=timezone.now())
            return Response({"message": "权限更新成功"})

        except Exception as e:
            return Response({
                "message": f"权限更新失败: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionDeleteView(APIView):
    @atomic_view
    def post(self, request, pk):
        try:
            root = Permission.objects.get(pk=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ 递归获取所有子权限
        def get_descendants(permission):
            children = Permission.objects.filter(parent_id=permission.id, is_deleted=0)
            descendants = list(children)
            for child in children:
                descendants.extend(get_descendants(child))
            return descendants

        all_permissions = [root] + get_descendants(root)
        ids = [p.id for p in all_permissions]

        # ✅ 删除权限本身（逻辑删除）
        Permission.objects.filter(id__in=ids).update(is_deleted=1, update_time=timezone.now())

        # ✅ 删除角色权限关联（物理删除）
        RolePermission.objects.filter(permission_id__in=ids).delete()

        return Response({"message": "权限及其子权限已删除，角色关联已清理"})
