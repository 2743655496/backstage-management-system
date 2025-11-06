from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from utils.decorators import atomic_view
from user_permission.models import Menu, Permission, RolePermission
from user_permission.serializers.menu_serializers import MenuSerializer, MenuTreeSerializer
from utils.serializer_errors import extract_error_message
from utils.validators import strict_validate_fields

# 在 views.py 顶部定义菜单字段验证规则
MENU_CREATE_SCHEMA = {
    "name": {
        "type": str,
        "required": True,
        "allow_blank": False
    },
    "icon": {
        "type": str,
        "required": False,
        "allow_blank": True
    },
    "path": {
        "type": str,
        "required": True,
        "allow_blank": False
    },
    "component": {
        "type": str,
        "required": True,
        "allow_blank": False
    },
    "sort": {
        "type": int,
        "required": True
    },
    "status": {
        "type": int,
        "required": True,
        "choices": [0, 1]
    },
    "visible": {
        "type": int,
        "required": True,
        "choices": [0, 1]
    },
    "parent_id": {
        "type": int,
        "required": False
    },
    "auto_permission": {
        "type": bool,
        "required": True
    }
}

MENU_UPDATE_SCHEMA = {
    "name": {
        "type": str,
        "required": False,
        "allow_blank": False
    },
    "icon": {
        "type": str,
        "required": False,
        "allow_blank": True
    },
    "path": {
        "type": str,
        "required": False,
        "allow_blank": False
    },
    "component": {
        "type": str,
        "required": False,
        "allow_blank": False
    },
    "sort": {
        "type": int,
        "required": False
    },
    "status": {
        "type": int,
        "required": False,
        "choices": [0, 1]
    },
    "visible": {
        "type": int,
        "required": False,
        "choices": [0, 1]
    },
}


class MenuListView(APIView):
    def get(self, request):
        """获取菜单树"""

        def build_tree(menu_list, parent_id=0):
            tree = []
            for menu in menu_list:
                if menu.parent_id == parent_id:
                    children = build_tree(menu_list, menu.id)
                    menu_data = MenuTreeSerializer(menu).data
                    menu_data['children'] = children
                    tree.append(menu_data)
            return sorted(tree, key=lambda x: x["sort"])

        menus = Menu.objects.filter(is_deleted=0).order_by("sort")
        tree = build_tree(list(menus))
        return Response({"data": tree})


class MenuCreateView(APIView):
    @atomic_view
    def post(self, request):
        """创建菜单"""
        # ✅ 前置字段验证
        error_response = strict_validate_fields(request.data, MENU_CREATE_SCHEMA)
        if error_response:
            return error_response
        serializer = MenuSerializer(data=request.data)

        if not serializer.is_valid():
            message = extract_error_message(serializer.errors)
            return Response({
                "message": message,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        auto_permission = validated_data.pop('auto_permission', False)

        try:
            # 创建菜单
            menu = Menu.objects.create(
                **validated_data,
                creator_id=request.my_user.id
            )

            # 自动创建权限
            if auto_permission:
                self._create_menu_permission(menu, request.my_user.id)

            return Response({
                "message": "菜单创建成功",
                "menu_id": menu.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": f"菜单创建失败: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _create_menu_permission(self, menu, creator_id):
        """创建菜单权限"""
        permission_code = f"menu:{menu.path.strip('/')}" if menu.path else f"menu:{menu.id}"
        permission_name = f"{menu.name}-页面权限"
        description = f"{menu.name}访问权限"

        permission_parent_id = 0
        if menu.parent_id != 0:
            parent_permission = Permission.objects.filter(
                menu_id=menu.parent_id, type=1, is_deleted=0
            ).first()
            permission_parent_id = parent_permission.id if parent_permission else 0

        permission = Permission.objects.create(
            name=permission_name,
            code=permission_code,
            description=description,
            type=1,
            menu_id=menu.id,
            parent_id=permission_parent_id,
            status=1,
            creator_id=creator_id
        )

        # 给默认角色（如管理员角色ID=1）分配权限
        RolePermission.objects.get_or_create(
            role_id=1,
            permission_id=permission.id,
            defaults={"creator_id": creator_id}
        )


class MenuUpdateView(APIView):
    @atomic_view
    def post(self, request, menu_id):
        """更新菜单"""
        # ✅ 前置字段验证
        error_response = strict_validate_fields(request.data, MENU_UPDATE_SCHEMA)
        if error_response:
            return error_response
        try:
            menu = Menu.objects.get(id=menu_id, is_deleted=0)
        except Menu.DoesNotExist:
            return Response({"error": "菜单不存在"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(menu, data=request.data, partial=True)

        if not serializer.is_valid():
            message = extract_error_message(serializer.errors)
            return Response({
                "message": message,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save(update_time=timezone.now())
            return Response({"message": "菜单更新成功"})

        except Exception as e:
            return Response({
                "message": f"菜单更新失败: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MenuDeleteView(APIView):
    @atomic_view
    def post(self, request, menu_id):
        """删除菜单"""
        try:
            root_menu = Menu.objects.get(id=menu_id, is_deleted=0)
        except Menu.DoesNotExist:
            return Response({"error": "菜单不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 获取所有子菜单（递归）
        def get_descendants(menu):
            descendants = []
            children = Menu.objects.filter(parent_id=menu.id, is_deleted=0)
            for child in children:
                descendants.append(child)
                descendants.extend(get_descendants(child))
            return descendants

        all_menus = [root_menu] + get_descendants(root_menu)
        menu_ids = [m.id for m in all_menus]

        # 批量逻辑删除菜单
        Menu.objects.filter(id__in=menu_ids).update(
            is_deleted=1,
            update_time=timezone.now()
        )

        # 删除关联权限
        permissions = Permission.objects.filter(menu_id__in=menu_ids, is_deleted=0)
        permission_ids = [p.id for p in permissions]

        Permission.objects.filter(id__in=permission_ids).update(
            is_deleted=1,
            update_time=timezone.now()
        )

        # 删除角色权限绑定
        RolePermission.objects.filter(permission_id__in=permission_ids).delete()

        return Response({"message": "菜单及其子菜单已删除，相关权限已清理"})