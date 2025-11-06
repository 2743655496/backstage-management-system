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


class RoleUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'code', 'description', 'status']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': '角色名称不能为空',
                    'max_length': '角色名称不能超过50个字符',
                    'unique': '角色名称已存在'  # 覆盖唯一性错误消息
                },
                "validators": []  # ✅ 禁用自动唯一性校验
            },
            'code': {
                'error_messages': {
                    'blank': '角色编码不能为空',
                    'max_length': '角色编码不能超过50个字符',
                    'unique': '角色编码已存在'  # 覆盖唯一性错误消息
                },
                "validators": []  # ✅ 禁用自动唯一性校验
            },
            'status': {
                'error_messages': {
                    'null': '角色状态不能为空',
                    'invalid': '角色状态值无效'
                }
            }
        }

    def validate_name(self, value):
        """验证角色名称"""
        # 检查是否为空
        if not value or not value.strip():
            raise serializers.ValidationError("角色名称不能为空")

        value = value.strip()

        # 检查长度
        if len(value) > 50:
            raise serializers.ValidationError("角色名称不能超过50个字符")

        # 验证唯一性
        if self.instance:
            # 更新操作，排除当前实例
            if Role.objects.filter(name=value, is_deleted=0).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("角色名称已存在")
        else:
            # 创建操作
            if Role.objects.filter(name=value, is_deleted=0).exists():
                raise serializers.ValidationError("角色名称已存在")

        return value

    def validate_code(self, value):
        """验证角色编码"""
        # 检查是否为空
        if not value or not value.strip():
            raise serializers.ValidationError("角色编码不能为空")

        value = value.strip()

        # 检查长度
        if len(value) > 50:
            raise serializers.ValidationError("角色编码不能超过50个字符")

        # 验证唯一性
        if self.instance:
            # 更新操作，排除当前实例
            if Role.objects.filter(code=value, is_deleted=0).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("角色编码已存在")
        else:
            # 创建操作
            if Role.objects.filter(code=value, is_deleted=0).exists():
                raise serializers.ValidationError("角色编码已存在")

        return value

    def validate_status(self, value):
        """验证角色状态"""
        # 检查是否为空
        if value is None:
            raise serializers.ValidationError("角色状态不能为空")

        # 检查状态值是否有效
        if value not in [0, 1]:
            raise serializers.ValidationError("角色状态只能为0(禁用)或1(启用)")

        return value

    def validate_description(self, value):
        """验证角色描述"""
        if value and len(value.strip()) > 255:
            raise serializers.ValidationError("角色描述不能超过255个字符")
        return value.strip() if value else value

    def validate(self, attrs):
        """全局验证"""
        # 这里可以添加跨字段的验证逻辑
        # 例如：如果某些字段组合需要特殊验证

        return attrs
