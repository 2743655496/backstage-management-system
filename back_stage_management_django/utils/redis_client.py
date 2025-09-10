# utils/redis_client.py
import redis
from django.conf import settings

class RedisClient:
    _pool = None

    @classmethod
    def get_connection(cls):
        """
        获取 Redis 连接（使用连接池）
        """
        if cls._pool is None:
            cls._pool = redis.ConnectionPool(
                host=getattr(settings, "REDIS_HOST", "127.0.0.1"),
                port=getattr(settings, "REDIS_PORT", 6379),
                db=getattr(settings, "REDIS_DB", 0),
                password=getattr(settings, "REDIS_PASSWORD", None),
                max_connections=getattr(settings, "REDIS_MAX_CONN", 100),
                decode_responses=True  # 自动解码为 str
            )
        return redis.Redis(connection_pool=cls._pool)

    @classmethod
    def set(cls, key, value, ex=None):
        """
        设置键值
        :param key: 键
        :param value: 值
        :param ex: 过期时间（秒）
        """
        return cls.get_connection().set(key, value, ex=ex)

    @classmethod
    def get(cls, key):
        """
        获取值
        """
        return cls.get_connection().get(key)

    @classmethod
    def incr(cls, key):
        """
        自增
        """
        return cls.get_connection().incr(key)

    @classmethod
    def expire(cls, key, seconds):
        """
        设置过期时间
        """
        return cls.get_connection().expire(key, seconds)

    @classmethod
    def delete(cls, key):
        """
        删除键
        """
        return cls.get_connection().delete(key)

    @classmethod
    def add_to_blacklist(cls, token, ttl):
        """
        将 token 加入黑名单
        :param token: 要拉黑的 JWT
        :param ttl: 有效期（秒），与 token 的剩余时间一致
        """
        key = f"blacklist:{token}"
        return cls.set(key, "1", ex=ttl)

    @classmethod
    def is_blacklisted(cls, token):
        """
        检查 token 是否在黑名单中
        """
        key = f"blacklist:{token}"
        return cls.get(key) is not None

