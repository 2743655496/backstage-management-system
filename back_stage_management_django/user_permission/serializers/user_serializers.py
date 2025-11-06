# serializers.py
from rest_framework import serializers
from user_permission.models import Department, UserRole, User, Role
from user_permission.utils.password_encode import secure_hash_password
import re


class UserUpdateCreateSerializer(serializers.ModelSerializer):
    """用户创建更新序列化器 - 专门用于创建更新用户"""
    role_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'real_name', 'email', 'phone',
            'department_id', 'status', 'role_ids', 'avatar'
        ]
        extra_kwargs = {
            'username': {
                'required': True,
                'allow_blank': False,
                'min_length': 3,
                'max_length': 50,
                'error_messages': {
                    'required': '用户名是必填项',
                    'blank': '用户名不能为空',
                    'min_length': '用户名长度不能少于3个字符',
                    'max_length': '用户名长度不能超过50个字符'
                }
            },
            'password': {
                'write_only': True,
                'required': True,
                'allow_blank': False,
                'min_length': 6,
                'error_messages': {
                    'required': '密码是必填项',
                    'blank': '密码不能为空',
                    'min_length': '密码长度不能少于6个字符'
                }
            },
            'real_name': {
                'required': False,
                'allow_blank': True,
                'allow_null': True,
                'max_length': 50,
                'error_messages': {
                    'max_length': '真实姓名不能超过50个字符'
                }
            },
            'email': {
                'required': False,
                'allow_blank': True,
                'allow_null': True,
                'max_length': 100,
                'error_messages': {
                    'invalid': '请输入正确的邮箱地址',
                    'max_length': '邮箱长度不能超过100个字符'
                }
            },
            'phone': {
                'required': False,
                'allow_blank': True,
                'allow_null': True,
                'max_length': 20,
                'error_messages': {
                    'max_length': '手机号长度不能超过20个字符'
                }
            },
            'status': {
                'required': True,
                'error_messages': {
                    'required': '状态是必填项',
                    'invalid': '状态值必须是整数'
                }
            },
            'avatar': {
                'required': False,
                'allow_blank': True,
                'allow_null': True,
                'max_length': 510,
                'error_messages': {
                    'max_length': '头像路径长度不能超过510个字符'
                }
            },
            'creator_id': {'read_only': True},
        }

    def create(self, validated_data):
        role_ids = validated_data.pop('role_ids', [])
        avatar_data = validated_data.get('avatar', '')

        # avatar 已在视图中处理为文件名或 URL，这里无需再处理
        validated_data['avatar'] = avatar_data

        # 加密密码
        if 'password' in validated_data and validated_data['password']:
            validated_data['password'] = secure_hash_password(validated_data['password'])
        else:
            raise serializers.ValidationError({'password': '密码是必填项'})

        # 设置创建人
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['creator_id'] = request.my_user.id

        # 创建用户
        user = User.objects.create(**validated_data)

        # 创建用户角色关联
        if role_ids:
            user_roles = [
                UserRole(user_id=user.id, role_id=role_id, creator_id=user.creator_id)
                for role_id in role_ids
            ]
            UserRole.objects.bulk_create(user_roles)

        return user

    def update(self, instance, validated_data):
        role_ids = validated_data.pop('role_ids', None)
        avatar_data = validated_data.get('avatar')

        # avatar 已在视图中处理为文件名或 URL，这里无需再处理
        validated_data['avatar'] = avatar_data

        # 密码加密（仅当传入）
        if 'password' in validated_data and validated_data['password']:
            validated_data['password'] = secure_hash_password(validated_data['password'])
        else:
            validated_data.pop('password', None)

        # 更新字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 更新角色关联
        if role_ids is not None:
            UserRole.objects.filter(user_id=instance.id).delete()
            user_roles = [
                UserRole(user_id=instance.id, role_id=role_id, creator_id=instance.creator_id)
                for role_id in role_ids
            ]
            UserRole.objects.bulk_create(user_roles)

        return instance

    def validate_password(self, value):
        """
        密码验证规则（与前端保持一致）：
        - 首字符必须为字母
        - 必须包含至少一个数字
        - 必须包含至少一个字母
        - 必须包含至少一个特殊字符 (!@#$%^&*)
        - 长度至少6位
        """
        if not value:
            raise serializers.ValidationError("请输入密码")

        # 检查首字符是否为字母
        if not re.match(r'^[a-zA-Z]', value):
            raise serializers.ValidationError("密码首字符必须为字母")

        # 检查是否包含数字
        if not re.search(r'\d', value):
            raise serializers.ValidationError("密码必须包含至少一个数字")

        # 检查是否包含字母
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("密码必须包含至少一个字母")

        # 检查是否包含特殊字符
        if not re.search(r'[!@#$%^&*]', value):
            raise serializers.ValidationError("密码必须包含至少一个特殊字符 (!@#$%^&*)")

        # 检查最小长度
        if len(value) < 6:
            raise serializers.ValidationError("密码长度不能少于6个字符")

        return value

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("请输入用户名")

        if len(value) < 3 or len(value) > 50:
            raise serializers.ValidationError("用户名长度为3-50个字符")

        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_real_name(self, value):
        if value and len(value) > 50:
            raise serializers.ValidationError("真实姓名不能超过50个字符")
        return value

    def validate_email(self, value):
        if value:
            # 使用更严格的邮箱验证
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
                raise serializers.ValidationError("请输入正确的邮箱地址")

            if len(value) > 100:
                raise serializers.ValidationError("邮箱长度不能超过100个字符")

            qs = User.objects.filter(email=value)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("邮箱已存在")
        return value

    def validate_phone(self, value):
        if value:
            # 使用与前端相同的手机号验证规则
            if not re.match(r'^1[3-9]\d{9}$', value):
                raise serializers.ValidationError("请输入正确的手机号码")

            if len(value) > 20:
                raise serializers.ValidationError("手机号长度不能超过20个字符")

            qs = User.objects.filter(phone=value)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("手机号已存在")
        return value

    def validate_status(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("状态值必须是0或1")
        return value

    def validate_department_id(self, value):
        if value is not None:
            # 验证部门是否存在
            if not Department.objects.filter(id=value).exists():
                raise serializers.ValidationError("指定的部门不存在")
        return value

    def validate_role_ids(self, value):
        if value:
            # 验证角色是否存在
            existing_roles = Role.objects.filter(id__in=value).values_list('id', flat=True)
            non_existing_roles = set(value) - set(existing_roles)
            if non_existing_roles:
                raise serializers.ValidationError(f"以下角色ID不存在: {', '.join(map(str, non_existing_roles))}")
        return value

    def validate_avatar(self, value):
        """只验证最终路径长度，不处理 base64"""
        if value and isinstance(value, str) and len(value) > 510:
            raise serializers.ValidationError("头像路径长度不能超过510个字符")
        return value

    def validate(self, attrs):
        """
        全局验证
        """
        # 如果是创建用户，密码是必填项
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': '创建用户时密码是必填项'})

        # 如果是更新用户，且传入了密码，需要验证密码
        if self.instance and attrs.get('password'):
            # 密码验证已经在 validate_password 方法中完成
            pass

        return attrs


class UserListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'real_name', 'email', 'phone',
            'department_id', 'department_name', 'status', 'last_login_time',
            'last_login_ip', 'creator_id', 'creator_name', 'create_time',
            'update_time', 'avatar', 'roles'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'creator_id': {'read_only': True},
            'last_login_time': {'read_only': True},
            'last_login_ip': {'read_only': True},
            'create_time': {'read_only': True},
            'update_time': {'read_only': True},
        }

    def get_department_name(self, obj):
        return getattr(obj, '_department_name', None)

    def get_creator_name(self, obj):
        return getattr(obj, '_creator_name', None)

    def get_avatar(self, obj):
        if obj.avatar:
            if obj.avatar.startswith(('http://', 'https://')):
                return obj.avatar
            return f'/avatars/{obj.avatar}'
        return '/avatars/default.png'

    def get_roles(self, obj):
        """获取用户角色列表"""
        return getattr(obj, '_roles', [])

    @classmethod
    def setup_eager_loading(cls, queryset):
        """预取部门、创建人、角色信息"""
        department_ids = set()
        creator_ids = set()
        user_ids = [user.id for user in queryset]

        for user in queryset:
            if user.department_id:
                department_ids.add(user.department_id)
            if user.creator_id:
                creator_ids.add(user.creator_id)

        departments = {dept.id: dept for dept in Department.objects.filter(id__in=department_ids)}
        creators = {creator.id: creator for creator in User.objects.filter(id__in=creator_ids)}

        # 批量获取角色信息
        user_roles = UserRole.objects.filter(user_id__in=user_ids)
        role_ids = set([ur.role_id for ur in user_roles])
        roles = {role.id: role for role in Role.objects.filter(id__in=role_ids)}

        # 构建 user_id -> [role_dict] 映射
        user_role_map = {}
        for ur in user_roles:
            role = roles.get(ur.role_id)
            if role:
                role_info = {
                    'id': role.id,
                    'name': role.name,
                    'code': role.code
                }
                user_role_map.setdefault(ur.user_id, []).append(role_info)

        # 设置缓存字段
        for user in queryset:
            if user.department_id in departments:
                user._department_name = departments[user.department_id].name
            if user.creator_id in creators:
                user._creator_name = creators[user.creator_id].username
            user._roles = user_role_map.get(user.id, [])

        return queryset


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name']