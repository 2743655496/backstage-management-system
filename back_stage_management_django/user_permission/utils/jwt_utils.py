import jwt
import datetime
from django.conf import settings
from user_permission.models import User  # 你的自定义用户模型
from django.utils import timezone

class JWTUtils:
    # 密钥，应该放在 settings 中
    SECRET_KEY = getattr(settings, 'JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    ALGORITHM = 'HS256'

    @classmethod
    def create_access_token(cls, user):
        """创建访问令牌"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': timezone.now() + datetime.timedelta(hours=1),  # 1小时过期
            'iat': timezone.now(),
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_refresh_token(cls, user, day_time ):
        """创建刷新令牌"""
        payload = {
            'user_id': user.id,
            'token_type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=day_time),  # 7天过期
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def verify_token(cls, token):
        """验证令牌"""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Token expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token')

    @classmethod
    def get_user_from_token(cls, token):
        """从令牌中获取用户"""
        try:
            payload = cls.verify_token(token)
            user_id = payload.get('user_id')
            if user_id:
                return User.objects.get(id=user_id, is_deleted=0)
            return None
        except (Exception, User.DoesNotExist):
            return None