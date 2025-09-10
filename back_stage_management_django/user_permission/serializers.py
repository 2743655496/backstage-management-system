from rest_framework import serializers
from .models import Department, Role, User, Permission
from user_permission.utils.password_encode import verify_secure_password
from utils.redis_client import RedisClient

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        ip = self.context.get('ip')

        cache_key = f"login_attempts:{username}:{ip}"
        attempts = int(RedisClient.get(cache_key) or 0)
        if attempts >= 5:
            raise serializers.ValidationError("尝试次数过多，请5分钟后再试")

        # 这里假设你的密码是明文存储的，如果是加密的，需要相应的验证逻辑
        try:
            user = User.objects.get(username=username, is_deleted=0)
        except User.DoesNotExist:
            # 用户不存在
            if not RedisClient.get(cache_key):
                RedisClient.set(cache_key, 1, ex=300)
            else:
                RedisClient.incr(cache_key)
                RedisClient.expire(cache_key, 300)
            raise serializers.ValidationError('用户不存在')

        # 检查用户状态
        if user.status != 1:
            raise serializers.ValidationError("用户已被禁用")

        # 简单的密码验证（根据你的实际存储方式调整）
        is_valid = verify_secure_password(password, user.password)  # True
        if not is_valid:  # 或者你的加密方式
            # 用户不存在
            if not RedisClient.get(cache_key):
                RedisClient.set(cache_key, 1, ex=300)
            else:
                RedisClient.incr(cache_key)
                RedisClient.expire(cache_key, 300)
            raise serializers.ValidationError('密码错误')

        attrs['user'] = user
        return attrs

    def _get_client_ip(self, request):
        """获取客户端真实 IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

