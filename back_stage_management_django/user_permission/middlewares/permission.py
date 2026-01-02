# middlewares/permission.py
import json
from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from utils.redis_client import RedisClient


class PermissionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # JWTAuthMiddleware 已经注入了 user
        user = getattr(request, 'my_user', None)
        if not user:
            # 未登录的情况交给 JWT 中间件处理，这里直接放行
            return None

        # 解析动态路由，得到规范化路径
        match = resolve(request.path)
        normalized_path = "/" + match.route      # 例：/api/system/permissions/update/<int:pk>/
        method = request.method.upper()

        # 从 Redis 获取权限缓存
        cache_key = f"user:permissions:tree:{user.id}"
        cached = RedisClient.get(cache_key)
        if not cached:
            # 正常情况是登录后就缓存好了，没有就提示重新登录或刷新权限
            return JsonResponse({
                "error": "权限缓存不存在",
                "detail": "请重新登录或联系管理员"
            }, status=403)

        data = json.loads(cached)
        api_permissions = data.get("api_permissions", {})
        # permission_codes = data.get("permission_codes", [])  # 预留：页面/按钮权限可用

        # 如果该接口在权限控制列表中，则进行校验
        if normalized_path in api_permissions:
            allowed_methods = api_permissions[normalized_path]
            if method not in allowed_methods:
                return JsonResponse({
                    "error": "无权限访问该接口",
                    "detail": f"需要权限：{normalized_path} [{method}]"
                }, status=403)

        # 不在 api_permissions 中的接口：默认放行（可按需调整策略）
        return None
