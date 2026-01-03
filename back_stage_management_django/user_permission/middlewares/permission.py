from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from utils.redis_client import RedisClient
from user_permission.services.permission_service import get_user_permissions
import json


class PermissionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = getattr(request, 'my_user', None)
        if not user:
            return None

        match = resolve(request.path)
        normalized_path = "/" + match.route
        method = request.method.upper()

        cache_key = f"user:permissions:tree:{user.id}"
        cached = RedisClient.get(cache_key)

        if cached:
            data = json.loads(cached)
        else:
            # ⭐ 缓存不存在 → 自动刷新权限缓存
            data = get_user_permissions(user.id)

        api_permissions = data.get("api_permissions", {})

        method_list = api_permissions.get(method, [])
        if normalized_path in method_list:
            return None

        all_paths = set(sum(api_permissions.values(), []))
        if normalized_path in all_paths:
            return JsonResponse({
                "error": "无权限访问该接口",
                "detail": f"需要权限：{normalized_path} [{method}]"
            }, status=403)

        return None
