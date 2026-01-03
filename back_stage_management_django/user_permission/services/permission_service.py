import json
from user_permission.models import UserRole, RolePermission, Permission, Menu
from utils.redis_client import RedisClient


def get_user_permissions(user_id):
    cache_key = f"user:permissions:tree:{user_id}"

    # 1. 先查缓存
    cached = RedisClient.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. 缓存不存在 → 重新生成
    role_ids = UserRole.objects.filter(user_id=user_id).values_list('role_id', flat=True)
    permission_ids = RolePermission.objects.filter(role_id__in=role_ids).values_list('permission_id', flat=True)

    permissions = Permission.objects.filter(
        id__in=permission_ids,
        status=1,
        is_deleted=0
    )

    # 菜单权限
    menu_ids = permissions.filter(type=1).values_list('menu_id', flat=True)
    menus = Menu.objects.filter(id__in=menu_ids, status=1, is_deleted=0).order_by('sort')

    menus_list = []

    def build_tree(menu_list, parent_id=0):
        tree = []
        for menu in menu_list:
            if menu.parent_id == parent_id:
                item = {
                    'id': menu.id,
                    'name': menu.name,
                    'path': menu.path,
                    'component': menu.component,
                    'icon': menu.icon,
                    'children': build_tree(menu_list, menu.id)
                }
                tree.append(item)

                if parent_id != 0:
                    menus_list.append({
                        'id': menu.id,
                        'name': menu.name,
                        'path': menu.path,
                        'component': menu.component,
                    })
        return tree

    menu_permissions = build_tree(list(menus))

    # 接口权限
    api_permissions = {
        "GET": [],
        "POST": [],
        "PUT": [],
        "DELETE": []
    }

    api_perms = permissions.filter(type=2).values("api_path", "api_method")

    for perm in api_perms:
        api_path = perm["api_path"]
        api_method = perm["api_method"].upper()

        if api_path and api_method in api_permissions:
            api_permissions[api_method].append(api_path)

    permission_codes = list(permissions.values_list("code", flat=True))

    result = {
        "menus_list": menus_list,
        "menu_permissions": menu_permissions,
        "api_permissions": api_permissions,
        "permission_codes": permission_codes
    }

    # 写入缓存
    RedisClient.set(cache_key, json.dumps(result), ex=1800)

    return result

