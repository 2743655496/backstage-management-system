from utils.redis_client import RedisClient
from user_permission.models import UserRole

def clear_role_users_permission_cache(role_id):
    """清除某个角色下所有用户的权限缓存"""
    user_ids = UserRole.objects.filter(role_id=role_id).values_list("user_id", flat=True)

    for user_id in user_ids:
        cache_key = f"user:permissions:tree:{user_id}"
        RedisClient.delete(cache_key)
