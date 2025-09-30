from user_permission.models import Department, Role, User, UserRole, RolePermission, Permission, Menu
from user_permission.serializers import PermissionSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




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

class PermissionDetailView(APIView):
    def get(self, request, pk):
        try:
            permission = Permission.objects.get(pk=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

class PermissionCreateView(APIView):
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator_id=request.user.id if request.user else None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionUpdateView(APIView):
    def put(self, request, pk):
        try:
            permission = Permission.objects.get(pk=pk, is_deleted=0)
        except Permission.DoesNotExist:
            return Response({"error": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(update_time=timezone.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionDeleteView(APIView):
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
