import jwt
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from user_permission.models import User

class JWTUtils:
    SECRET_KEY = getattr(settings, 'JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    ALGORITHM = 'HS256'

    @classmethod
    def create_access_token(cls, user ,hours_time):
        """创建访问令牌（1小时有效）"""
        now = timezone.now()
        payload = {
            'user_id': user.id,
            'username': user.username,
            'token_type': 'access',
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(hours=hours_time)).timestamp())
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_refresh_token(cls, user, day_time):
        """创建刷新令牌（day_time天有效）"""
        now = timezone.now()
        payload = {
            'user_id': user.id,
            'token_type': 'refresh',
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(days=day_time)).timestamp())
            # 'exp': int((now + timedelta(seconds=600)).timestamp())
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
