# serializers.py
from rest_framework import serializers
from user_permission.models import Department, UserRole, User,Role
from user_permission.utils.password_encode import secure_hash_password



class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器 - 专门用于创建用户"""
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
            'password': {'write_only': True, 'required': True},
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
        if len(value) < 6:
            raise serializers.ValidationError("密码长度不能少于6个字符")
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("用户名长度不能少于3个字符")

        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_email(self, value):
        if value:
            if '@' not in value:
                raise serializers.ValidationError("请输入有效的邮箱地址")

            qs = User.objects.filter(email=value)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("邮箱已存在")
        return value

    def validate_phone(self, value):
        if value:
            if not value.isdigit() or len(value) != 11:
                raise serializers.ValidationError("请输入有效的手机号码")

            qs = User.objects.filter(phone=value)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("手机号已存在")
        return value

    def validate_avatar(self, value):
        """只验证最终路径长度，不处理 base64"""
        if value and isinstance(value, str) and len(value) > 255:
            raise serializers.ValidationError("头像路径长度不能超过255个字符")
        return value


class UserListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()  # ✅ 新增字段：角色列表

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'real_name', 'email', 'phone',
            'department_id', 'department_name', 'status', 'last_login_time',
            'last_login_ip', 'creator_id', 'creator_name', 'create_time',
            'update_time', 'avatar', 'roles'  # ✅ 添加 roles 字段
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

        # ✅ 批量获取角色信息
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
