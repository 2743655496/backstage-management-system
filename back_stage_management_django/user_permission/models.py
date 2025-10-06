from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='部门名称')
    parent_id = models.BigIntegerField(default=0, verbose_name='父部门ID')
    code = models.CharField(max_length=50, unique=True, verbose_name='部门编码')
    description = models.TextField(blank=True, null=True, verbose_name='部门描述')
    manager_id = models.BigIntegerField(blank=True, null=True, verbose_name='部门负责人ID')
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.SmallIntegerField(default=1, verbose_name='状态(1启用，0禁用)')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='删除标志(0未删除,1删除)')

    class Meta:
        db_table = 'departments'
        verbose_name = '部门'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['parent_id']),
            models.Index(fields=['status']),
        ]


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='角色编码')
    description = models.TextField(blank=True, null=True, verbose_name='角色描述')
    status = models.SmallIntegerField(default=1, verbose_name='状态(0禁用,1启用)')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='删除标志状态(0未删除,1删除)')

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['status']),
        ]


class User(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    real_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='真实姓名')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像')
    department_id = models.BigIntegerField(blank=True, null=True, verbose_name='所属部门ID')
    status = models.SmallIntegerField(default=1, verbose_name='状态(0禁用,1启用)')
    last_login_time = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')
    last_login_ip = models.CharField(max_length=50, blank=True, null=True, verbose_name='最后登录IP')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='删除标志(0未删除,1删除)')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['department_id']),
            models.Index(fields=['status']),
        ]


class UserRole(models.Model):
    user_id = models.BigIntegerField(verbose_name='用户ID')
    role_id = models.BigIntegerField(verbose_name='角色ID')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'user_roles'
        verbose_name = '用户角色关联'
        unique_together = ('user_id', 'role_id')
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['role_id']),
        ]


class Menu(models.Model):
    parent_id = models.BigIntegerField(default=0, verbose_name='父菜单ID（0目录）')
    name = models.CharField(max_length=50, verbose_name='菜单名称')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='菜单图标')
    path = models.CharField(max_length=100, blank=True, null=True, verbose_name='路由路径')
    component = models.CharField(max_length=100, blank=True, null=True, verbose_name='组件路径')
    sort = models.IntegerField(default=0, verbose_name='排序')
    visible = models.SmallIntegerField(default=1, verbose_name='是否显示')
    status = models.SmallIntegerField(default=1, verbose_name='状态(0禁用,1启用)')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='删除标志(0未删除,1删除)')

    class Meta:
        db_table = 'menus'
        verbose_name = '菜单'
        indexes = [
            models.Index(fields=['parent_id']),
            models.Index(fields=['sort']),
            models.Index(fields=['status']),
        ]


class Permission(models.Model):
    PERMISSION_TYPE_CHOICES = (
        (1, '菜单权限'),
        (2, '接口权限'),
        (3, '按钮权限'),
    )
    name = models.CharField(max_length=50, verbose_name='权限名称')
    code = models.CharField(max_length=100, unique=True, verbose_name='权限标识')
    description = models.TextField(blank=True, null=True, verbose_name='权限描述')
    type = models.SmallIntegerField(choices=PERMISSION_TYPE_CHOICES, verbose_name='权限类型')
    menu_id = models.BigIntegerField(blank=True, null=True, verbose_name='关联菜单ID(仅菜单权限需要)')
    parent_id = models.BigIntegerField(default=0, verbose_name='父权限ID')
    api_method = models.CharField(max_length=10, blank=True, null=True, verbose_name='接口方法')
    api_path = models.CharField(max_length=255, blank=True, null=True, verbose_name='接口路径')
    status = models.SmallIntegerField(default=1, verbose_name='状态(0禁用,1启用)')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='删除标志(0未删除,1删除)')

    class Meta:
        db_table = 'permissions'
        verbose_name = '权限'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['type']),
            models.Index(fields=['menu_id']),
            models.Index(fields=['parent_id']),
            models.Index(fields=['status']),
        ]


class RolePermission(models.Model):
    role_id = models.BigIntegerField(verbose_name='角色ID')
    permission_id = models.BigIntegerField(verbose_name='权限ID')
    creator_id = models.BigIntegerField(blank=True, null=True, verbose_name='创建人ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'role_permissions'
        verbose_name = '角色权限关联'
        unique_together = ('role_id', 'permission_id')
        indexes = [
            models.Index(fields=['role_id']),
            models.Index(fields=['permission_id']),
        ]
