# middlewares/jwt_auth.py
from django.utils import timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from user_permission.utils.jwt_utils import JWTUtils
from utils.redis_client import RedisClient
from .whitelist import PUBLIC_WHITELIST


class JWTAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path.rstrip("/")  # 统一去掉尾斜杠
        method = request.method.upper()

        # ① PUBLIC 白名单（无需登录）
        if path in PUBLIC_WHITELIST:
            allowed = PUBLIC_WHITELIST[path]
            if allowed == "*" or method in allowed:
                return None

        # -------------------------
        # ② 获取 Token
        # -------------------------
        token = request.COOKIES.get('access_token')
        if not token:
            return JsonResponse({'error': '未提供令牌', 'detail': '请登录后访问'}, status=401)

        # 黑名单校验
        if RedisClient.is_blacklisted(token):
            return JsonResponse({'error': '令牌已失效', 'detail': '该令牌已被撤销或登出'}, status=401)

        try:
            payload = JWTUtils.verify_token(token)
            user = JWTUtils.get_user_from_token(token)

            if not user:
                return JsonResponse({'error': '认证失败', 'detail': '用户不存在或令牌无效'}, status=401)

            request.my_user = user

            exp_timestamp = payload.get('exp')
            if exp_timestamp:
                now = timezone.now().timestamp()
                request.access_token_expires_in = int(exp_timestamp - now)

            return None

        except Exception as e:
            return JsonResponse({'error': '认证错误', 'detail': str(e)}, status=401)
