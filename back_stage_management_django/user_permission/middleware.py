# middleware.py
import re
from django.utils import timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .utils.jwt_utils import JWTUtils  # 你的 JWT 工具类
from utils.redis_client import RedisClient


class JWTAuthMiddleware(MiddlewareMixin):
    # 定义白名单路径（不需要认证的接口）
    WHITELIST_PATHS = [
        r'^/api/system/auth/login/$',  # 登录接口
        r'^/api/system/auth/slider_verify/$',  # 滑块验证接口
        r'^/api/system/auth/refresh/$',  # token刷新接口
        # r'^/admin/',  # Django 后台管理
        # r'^/health/$',  # 健康检查端点
        # 添加其他需要排除的路径...
    ]

    def process_request(self, request):
        # 获取请求路径
        path = request.path

        # 检查是否在白名单中
        if any(re.match(pattern, path) for pattern in self.WHITELIST_PATHS):
            return None  # 跳过认证

        # 从请求头中获取 JWT Token
        # auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        #
        # if not auth_header.startswith('Bearer '):
        #     return JsonResponse({
        #         'error': '未提供认证令牌',
        #         'detail': '请在请求头中包含 Authorization: Bearer <token>'
        #     }, status=401)

        # token = auth_header[7:]  # 提取 Token

        # 使用 HttpOnly Cookie
        token = request.COOKIES.get('access_token')
        if not token:
            return JsonResponse({
                'error': '未提供令牌',
                'detail': '请登录后访问'
            }, status=401)
        # 黑名单校验
        if RedisClient.is_blacklisted(token):
            return JsonResponse({
                'error': '令牌已失效',
                'detail': '该令牌已被撤销或登出'
            }, status=401)
        try:
            # ✅ 解码 token 获取 payload
            payload = JWTUtils.verify_token(token)
            # 验证 Token 并获取用户
            user = JWTUtils.get_user_from_token(token)
            if not user:
                return JsonResponse({
                    'error': '认证失败',
                    'detail': '用户不存在或令牌无效'
                }, status=401)

            # ✅ 注入用户对象
            request.my_user = user

            # ✅ 注入 access_token 剩余时间
            # ✅ 使用 Django 的 timezone.now() 计算剩余时间
            exp_timestamp = payload.get('exp')
            if exp_timestamp:
                now = timezone.now().timestamp()
                request.access_token_expires_in = int(exp_timestamp - now)

            return None
        except Exception as e:
            return JsonResponse({
                'error': '认证错误',
                'detail': str(e)
            }, status=401)