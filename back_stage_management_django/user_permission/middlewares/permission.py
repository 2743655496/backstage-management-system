# middlewares/permission.py
import json
from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from utils.redis_client import RedisClient
from user_permission.services.permission_service import get_user_permissions
from .whitelist import (
    PUBLIC_WHITELIST,
    LOGIN_ONLY_WHITELIST,
    LOGIN_ONLY_PREFIX
)

class PermissionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path.rstrip("/")
        method = request.method.upper()

        # ① PUBLIC 白名单（无需登录、无需权限）
        if path in PUBLIC_WHITELIST:
            allowed = PUBLIC_WHITELIST[path]
            if allowed == "*" or method in allowed:
                return None

        # ② 未登录 → 401（JWT 中间件兜底）
        user = getattr(request, 'my_user', None)
        if not user:
            return JsonResponse({"error": "未登录"}, status=401)

        # ③ LOGIN_ONLY 白名单（需要登录，但无需权限）
        if path in LOGIN_ONLY_WHITELIST:
            allowed = LOGIN_ONLY_WHITELIST[path]
            if allowed == "*" or method in allowed:
                return None

        # ④ LOGIN_ONLY 动态路径白名单
        for prefix, allowed_methods in LOGIN_ONLY_PREFIX.items():
            if path.startswith(prefix):
                if allowed_methods == "*" or method in allowed_methods:
                    return None

        # ⑤ 解析路由（不存在 → 404）
        try:
            match = resolve(request.path)
        except Exception:
            return None

        normalized_path = "/" + match.route

        # ⑥ 权限判断
        cache_key = f"user:permissions:tree:{user.id}"
        cached = RedisClient.get(cache_key)
        data = json.loads(cached) if cached else get_user_permissions(user.id)

        api_permissions = data.get("api_permissions", {})
        method_list = api_permissions.get(method, [])

        if normalized_path in method_list:
            return None

        return JsonResponse({
            "error": "无权限访问该接口",
            "detail": f"需要权限：{normalized_path} [{method}]"
        }, status=403)
