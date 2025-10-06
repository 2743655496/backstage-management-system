from rest_framework import serializers
from user_permission.models import Role, User


class RoleSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'code', 'description', 'status',
            'status_display', 'creator_id', 'creator_name',
            'create_time', 'update_time'
        ]
        read_only_fields = ['id', 'create_time', 'update_time']

    def get_creator_name(self, obj):
        """获取创建人姓名"""
        if obj.creator_id:
            try:
                user = User.objects.get(id=obj.creator_id)
                return user.real_name or user.username
            except User.DoesNotExist:
                return None
        return None

    def get_status_display(self, obj):
        """获取状态显示文本"""
        return "启用" if obj.status == 1 else "禁用"

    def validate_name(self, value):
        """验证角色名称唯一性"""
        if self.instance and self.instance.name == value:
            return value

        if Role.objects.filter(name=value, is_deleted=0).exists():
            raise serializers.ValidationError("角色名称已存在")
        return value

    def validate_code(self, value):
        """验证角色编码唯一性"""
        if self.instance and self.instance.code == value:
            return value

        if Role.objects.filter(code=value, is_deleted=0).exists():
            raise serializers.ValidationError("角色编码已存在")
        return value


class RoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'code', 'description', 'status']

    def validate_name(self, value):
        if Role.objects.filter(name=value, is_deleted=0).exists():
            raise serializers.ValidationError("角色名称已存在")
        return value

    def validate_code(self, value):
        if Role.objects.filter(code=value, is_deleted=0).exists():
            raise serializers.ValidationError("角色编码已存在")
        return value


class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'code', 'description', 'status']

    def validate_name(self, value):
        if self.instance and self.instance.name == value:
            return value

        if Role.objects.filter(name=value, is_deleted=0).exists():
            raise serializers.ValidationError("角色名称已存在")
        return value

    def validate_code(self, value):
        if self.instance and self.instance.code == value:
            return value

        if Role.objects.filter(code=value, is_deleted=0).exists():
            raise serializers.ValidationError("角色编码已存在")
        return value