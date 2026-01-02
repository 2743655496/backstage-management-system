# middlewares/jwt_auth.py
import re
from django.utils import timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from user_permission.utils.jwt_utils import JWTUtils
from utils.redis_client import RedisClient


class JWTAuthMiddleware(MiddlewareMixin):
    WHITELIST_PATHS = [
        r'^/api/system/auth/login/$',
        r'^/api/system/auth/slider_verify/$',
        r'^/api/system/auth/refresh/$',
    ]

    def process_request(self, request):
        path = request.path

        # 白名单直接放行
        if any(re.match(pattern, path) for pattern in self.WHITELIST_PATHS):
            return None

        # 从 Cookie 获取 Token
        token = request.COOKIES.get('access_token')
        if not token:
            return JsonResponse({'error': '未提供令牌', 'detail': '请登录后访问'}, status=401)

        # 黑名单校验
        if RedisClient.is_blacklisted(token):
            return JsonResponse({'error': '令牌已失效', 'detail': '该令牌已被撤销或登出'}, status=401)

        try:
            # 解析 token
            payload = JWTUtils.verify_token(token)

            # 获取用户
            user = JWTUtils.get_user_from_token(token)
            if not user:
                return JsonResponse({'error': '认证失败', 'detail': '用户不存在或令牌无效'}, status=401)

            # 注入用户
            request.my_user = user

            # 注入 token 剩余时间
            exp_timestamp = payload.get('exp')
            if exp_timestamp:
                now = timezone.now().timestamp()
                request.access_token_expires_in = int(exp_timestamp - now)

            return None

        except Exception as e:
            return JsonResponse({'error': '认证错误', 'detail': str(e)}, status=401)
