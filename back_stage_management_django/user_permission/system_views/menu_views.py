from user_permission.models import RolePermission, Permission, Menu
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MenuListView(APIView):
    def get(self, request):
        def build_tree(menu_list, parent_id=0):
            tree = []
            for menu in menu_list:
                if menu.parent_id == parent_id:
                    children = build_tree(menu_list, menu.id)
                    tree.append({
                        "id": menu.id,
                        "name": menu.name,
                        "icon": menu.icon,
                        "path": menu.path,
                        "component": menu.component,
                        "sort": menu.sort,
                        "status": menu.status,
                        "visible": menu.visible,
                        "children": children,
                        "parent_id": menu.parent_id,
                    })
            return sorted(tree, key=lambda x: x["sort"])

        menus = Menu.objects.filter(is_deleted=0).order_by("sort")
        tree = build_tree(list(menus))
        return Response({"data": tree})


class MenuCreateView(APIView):
    def post(self, request):
        data = request.data
        # ✅ 唯一性校验：菜单名称
        if Menu.objects.filter(name=data["name"], is_deleted=0).exists():
            return Response({"message": "菜单名称已存在"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 唯一性校验：路由路径
        path = data.get("path")
        if Menu.objects.filter(path=path, is_deleted=0).exists():
            return Response({"message": "路由路径已存在"}, status=status.HTTP_400_BAD_REQUEST)
        menu = Menu.objects.create(
            parent_id=data.get("parent_id", 0),
            name=data["name"],
            icon=data.get("icon"),
            path=data.get("path"),
            component=data.get("component"),
            sort=data.get("sort", 0),
            status=data.get("status", 1),
            creator_id=request.my_user.id
        )
        auto_permission = data.get("auto_permission")
        if auto_permission:
            # 自动生成权限标识（可根据路径或菜单名生成）
            permission_code = f"menu:{menu.path.strip('/')}" if menu.path else f"menu:{menu.id}"
            permission_name = f"{menu.name}-页面权限"
            description = f"{menu.name}访问权限"
            permission_parent_id = 0
            if menu.parent_id != 0:
                # 查询父菜单对应的权限（菜单权限类型）
                parent_permission = Permission.objects.filter(
                    menu_id=menu.parent_id,
                    type=1,
                    is_deleted=0
                ).first()
                permission_parent_id = parent_permission.id if parent_permission else 0
            # 创建权限记录
            permission = Permission.objects.create(
                name=permission_name,
                code=permission_code,
                description=description,
                type=1,  # 菜单权限
                menu_id=menu.id,
                parent_id=permission_parent_id,
                status=1,
                creator_id=request.my_user.id
            )

            # 分配给超级管理员角色（假设角色ID为1）
            RolePermission.objects.get_or_create(
                role_id=1,
                permission_id=permission.id,
                defaults={"creator_id": request.my_user.id}
            )

        return Response({"message": "菜单创建成功", "menu_id": menu.id}, status=status.HTTP_201_CREATED)


class MenuUpdateView(APIView):
    def post(self, request, menu_id):
        data = request.data
        try:
            menu = Menu.objects.get(id=menu_id, is_deleted=0)
        except Menu.DoesNotExist:
            return Response({"error": "菜单不存在"}, status=status.HTTP_404_NOT_FOUND)
        # ✅ 唯一性校验：菜单名称
        new_name = data.get("name")
        if new_name and Menu.objects.filter(name=new_name, is_deleted=0).exclude(id=menu_id).exists():
            return Response({"message": "菜单名称已存在"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 唯一性校验：路由路径
        new_path = data.get("path")
        if Menu.objects.filter(path=new_path, is_deleted=0).exclude(id=menu_id).exists():
            return Response({"message": "路由路径已存在"}, status=status.HTTP_400_BAD_REQUEST)
        for field in ["name", "icon", "path", "component", "sort", "status"]:
            if field in data:
                setattr(menu, field, data[field])
        menu.update_time = timezone.now()
        menu.save()

        return Response({"message": "菜单更新成功"})


class MenuDeleteView(APIView):
    def post(self, request, menu_id):
        try:
            root_menu = Menu.objects.get(id=menu_id, is_deleted=0)
        except Menu.DoesNotExist:
            return Response({"error": "菜单不存在"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ 获取所有子菜单（递归）
        def get_descendants(menu):
            descendants = []
            children = Menu.objects.filter(parent_id=menu.id, is_deleted=0)
            for child in children:
                descendants.append(child)
                descendants.extend(get_descendants(child))
            return descendants

        all_menus = [root_menu] + get_descendants(root_menu)
        menu_ids = [m.id for m in all_menus]

        # ✅ 批量逻辑删除菜单
        Menu.objects.filter(id__in=menu_ids).update(is_deleted=1, update_time=timezone.now())

        # ✅ 删除关联权限
        permissions = Permission.objects.filter(menu_id__in=menu_ids)
        permission_ids = [p.id for p in permissions]

        Permission.objects.filter(id__in=permission_ids).update(is_deleted=1, update_time=timezone.now())

        # ✅ 删除角色权限绑定
        RolePermission.objects.filter(permission_id__in=permission_ids).delete()

        return Response({"message": "菜单及其子菜单已删除，相关权限已清理"})
