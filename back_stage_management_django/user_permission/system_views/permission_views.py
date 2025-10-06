from user_permission.models import Department, Role, User, UserRole, RolePermission, Permission, Menu
from user_permission.serializers.permission_serializers import PermissionSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.serializer_errors import extract_error_message
from utils.decorators import atomic_view

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
        try:
            permission = Permission.objects.get(id=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # ✅ 权限标识唯一性校验（排除当前记录）
        new_code = data.get("code")
        if new_code and Permission.objects.filter(code=new_code, is_deleted=0).exclude(id=pk).exists():
            return Response({"message": "权限标识已存在"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 通用字段更新
        for field in ["name", "code", "description", "type", "parent_id", "status"]:
            if field in data:
                setattr(permission, field, data[field])

        # ✅ 菜单权限字段更新
        if data.get("type") == 1:
            permission.menu_id = data.get("menu_id")

        # ✅ 接口权限字段更新
        if data.get("type") == 2:
            permission.api_method = data.get("api_method")
            permission.api_path = data.get("api_path")

        # ✅ 清除无关字段（防止残留）
        if data.get("type") != 1:
            permission.menu_id = None
        if data.get("type") != 2:
            permission.api_method = None
            permission.api_path = None

        permission.update_time = timezone.now()
        permission.save()

        return Response({"message": "权限更新成功"}, status=status.HTTP_200_OK)



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
