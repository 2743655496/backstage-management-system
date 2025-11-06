from rest_framework import serializers
from user_permission.models import Menu, Permission, RolePermission


class MenuSerializer(serializers.ModelSerializer):
    auto_permission = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Menu
        fields = [
            'id', 'parent_id', 'name', 'icon', 'path', 'component',
            'sort', 'visible', 'status', 'auto_permission'
        ]
        read_only_fields = ['id', 'create_time', 'update_time']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': '请输入菜单名称',
                    'max_length': '菜单名称长度不能超过50个字符'
                }
            },
            'icon': {
                'required': False,
                'allow_blank': True,
                'error_messages': {
                    'max_length': '图标名称不能超过50个字符'
                }
            },
            'path': {
                'error_messages': {
                    'blank': '路由路径不能为空',
                    'max_length': '路由路径不能超过100个字符'
                }
            },
            'component': {
                'error_messages': {
                    'blank': '组件路径不能为空',
                    'max_length': '组件路径不能超过100个字符'
                }
            },
            'sort': {
                'error_messages': {
                    'invalid': '请输入排序值'
                }
            }
        }

    def validate_name(self, value):
        """验证菜单名称"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("请输入菜单名称")

        if len(value) > 50:
            raise serializers.ValidationError("菜单名称长度不能超过50个字符")

        # 排除当前实例（在更新时使用）
        instance = getattr(self, 'instance', None)
        queryset = Menu.objects.filter(name=value, is_deleted=0)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError("菜单名称已存在")

        return value.strip()

    def validate_icon(self, value):
        """验证图标名称"""
        if value and len(value) > 50:
            raise serializers.ValidationError("图标名称不能超过50个字符")
        return value

    def validate_path(self, value):
        """验证路由路径"""
        if not value:
            raise serializers.ValidationError("路由路径不能为空")

        if len(value) > 100:
            raise serializers.ValidationError("路由路径不能超过100个字符")

        # 路径格式验证
        import re
        pattern = r'^\/[a-zA-Z0-9/_-]*$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "路由路径必须以 / 开头，只能包含字母、数字、下划线、- 和 /"
            )

        # 唯一性验证
        instance = getattr(self, 'instance', None)
        queryset = Menu.objects.filter(path=value, is_deleted=0)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError("路由路径已存在")

        return value

    def validate_component(self, value):
        """验证组件路径"""
        if not value:
            raise serializers.ValidationError("组件路径不能为空")

        if len(value) > 100:
            raise serializers.ValidationError("组件路径不能超过100个字符")

        # 组件路径格式验证
        import re
        pattern = r'^[a-zA-Z0-9/_-]+$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("组件路径只能包含字母、数字、下划线、- 和 /")

        return value

    def validate_sort(self, value):
        """验证排序值"""
        if value is None:
            raise serializers.ValidationError("请输入排序值")

        if value < 0:
            raise serializers.ValidationError("排序必须为非负整数")

        return value

    def validate_visible(self, value):
        """验证是否显示"""
        if value not in [0, 1]:
            raise serializers.ValidationError("请选择是否显示")
        return value

    def validate_status(self, value):
        """验证菜单状态"""
        if value not in [0, 1]:
            raise serializers.ValidationError("请选择菜单状态")
        return value

    def validate_parent_id(self, value):
        """验证父菜单ID"""
        if value != 0:
            try:
                parent_menu = Menu.objects.get(id=value, is_deleted=0)
                # 防止循环引用
                if self.instance and self.instance.id == value:
                    raise serializers.ValidationError("不能选择自己作为父菜单")
            except Menu.DoesNotExist:
                raise serializers.ValidationError("父菜单不存在")
        return value


class MenuTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'icon', 'path', 'component', 'sort',
            'status', 'visible', 'children', 'parent_id'
        ]

    def get_children(self, obj):
        """递归获取子菜单"""
        children = Menu.objects.filter(parent_id=obj.id, is_deleted=0).order_by('sort')
        return MenuTreeSerializer(children, many=True).data