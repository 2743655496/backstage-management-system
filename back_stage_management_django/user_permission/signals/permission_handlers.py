from django.dispatch import receiver
from .permission_signals import permissions_changed
from utils.redis_client import RedisClient

@receiver(permissions_changed)
def refresh_permissions_cache(sender, user_ids=None, **kwargs):
    """自动刷新用户权限缓存"""
    if not user_ids:
        return

    for uid in user_ids:
        cache_key = f"user:permissions:tree:{uid}"
        RedisClient.delete(cache_key)
