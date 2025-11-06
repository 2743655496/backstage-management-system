from rest_framework import serializers
from user_permission.models import User, Permission, Menu
import re


class PermissionSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'code',
            'description',
            'type',
            'menu_id',
            'parent_id',
            'api_method',
            'api_path',
            'status',
            'creator_id',
            'creator',
            'create_time',
            'update_time',
        ]
        read_only_fields = ['id', 'creator_id', 'creator', 'create_time', 'update_time']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': '请输入权限名称',
                    'max_length': '权限名称不能超过50个字符'
                }
            },
            'code': {
                'error_messages': {
                    'blank': '请输入权限标识',
                    'max_length': '权限标识不能超过100个字符'
                }
            },
            'description': {
                'error_messages': {
                    'max_length': '权限描述不能超过255个字符'
                }
            }
        }

    def validate_name(self, value):
        """验证权限名称"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("请输入权限名称")

        value = value.strip()
        if len(value) > 50:
            raise serializers.ValidationError("权限名称不能超过50个字符")

        # 排除当前实例（在更新时使用）
        instance = getattr(self, 'instance', None)
        queryset = Permission.objects.filter(name=value, is_deleted=0)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError("权限名称已存在")

        return value

    def validate_code(self, value):
        """验证权限标识"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("请输入权限标识")

        value = value.strip()
        if len(value) > 100:
            raise serializers.ValidationError("权限标识不能超过100个字符")

        # 格式验证
        if not re.match(r'^[a-zA-Z0-9:_-]+$', value):
            raise serializers.ValidationError("只能包含字母、数字、冒号、下划线、短横线")

        # 唯一性验证
        instance = getattr(self, 'instance', None)
        queryset = Permission.objects.filter(code=value, is_deleted=0)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError("权限标识已存在")

        return value

    def validate_type(self, value):
        """验证权限类型"""
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("请选择有效的权限类型")
        return value

    def validate_description(self, value):
        """验证权限描述"""
        if value and len(value) > 255:
            raise serializers.ValidationError("权限描述不能超过255个字符")
        return value

    def validate_menu_id(self, value):
        """验证关联菜单"""
        if value is not None:
            try:
                menu = Menu.objects.get(id=value, is_deleted=0)
            except Menu.DoesNotExist:
                raise serializers.ValidationError("关联菜单不存在")
        return value

    def validate_parent_id(self, value):
        """验证父权限"""
        if value and value != 0:
            try:
                parent = Permission.objects.get(id=value, is_deleted=0)
                # 防止循环引用
                if self.instance and self.instance.id == value:
                    raise serializers.ValidationError("不能选择自己作为父权限")
            except Permission.DoesNotExist:
                raise serializers.ValidationError("父权限不存在")
        return value

    def validate_api_method(self, value):
        """验证接口方法"""
        if value and value not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
            raise serializers.ValidationError("请选择有效的接口方法")
        return value

    def validate_api_path(self, value):
        """验证接口路径"""
        if value and len(value) > 255:
            raise serializers.ValidationError("接口路径不能超过255个字符")
        return value

    def validate_status(self, value):
        """验证状态"""
        if value not in [0, 1]:
            raise serializers.ValidationError("请选择有效的状态")
        return value

    def validate(self, attrs):
        """全局验证"""
        errors = {}

        permission_type = attrs.get('type')
        if permission_type is None and self.instance:
            permission_type = self.instance.type

        # 菜单权限必须关联菜单
        if permission_type == 1:
            menu_id = attrs.get('menu_id')
            if not menu_id and (not self.instance or not self.instance.menu_id):
                errors['menu_id'] = ['请选择关联菜单']

        # 接口权限必须填写接口方法和路径
        if permission_type == 2:
            api_method = attrs.get('api_method')
            api_path = attrs.get('api_path')

            if not api_method and (not self.instance or not self.instance.api_method):
                errors['api_method'] = ['请选择接口方法']

            if not api_path and (not self.instance or not self.instance.api_path):
                errors['api_path'] = ['请输入接口路径']

        # 清理无关字段
        if permission_type != 1:
            attrs['menu_id'] = None
        if permission_type != 2:
            attrs['api_method'] = None
            attrs['api_path'] = None

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def get_creator(self, obj):
        try:
            user = User.objects.get(id=obj.creator_id)
            return {
                "id": user.id,
                "username": user.username,
                "real_name": user.real_name,
            }
        except User.DoesNotExist:
            return None