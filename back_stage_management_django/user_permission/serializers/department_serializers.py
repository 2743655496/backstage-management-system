from rest_framework import serializers
from user_permission.models import Department, User


class DepartmentSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            "id", "name", "code", "description", "parent_id", "manager_id", "manager",
            "sort", "status", "creator_id", "creator", "create_time", "update_time"
        ]
        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
                "max_length": 50,
                "error_messages": {
                    "required": "请输入部门名称",
                    "blank": "请输入部门名称",
                    "max_length": "部门名称不能超过50个字符"
                },
                "validators": []  # ✅ 禁用自动唯一性校验
            },
            "code": {
                "required": True,
                "max_length": 50,
                "allow_blank": False,
                "error_messages": {
                    "required": "请输入部门编码",
                    "blank": "请输入部门编码",
                    "max_length": "部门编码不能超过50个字符"
                },
                "validators": []  # ✅ 禁用自动唯一性校验
            },
            "description": {
                "max_length": 255,
                "error_messages": {
                    "max_length": "部门描述不能超过255个字符"
                }
            },
            "sort": {
                "required": True,
                "error_messages": {
                    "required": "请输入排序值",
                    "invalid": "排序值必须为整数"
                }
            },
            "status": {
                "required": True,
                "error_messages": {
                    "required": "请选择状态",
                    "invalid": "状态值无效"
                }
            }
        }

    def get_creator(self, obj):
        try:
            user = User.objects.get(id=obj.creator_id)
            return {"id": user.id, "username": user.username, "real_name": user.real_name}
        except User.DoesNotExist:
            return None

    def get_manager(self, obj):
        try:
            user = User.objects.get(id=obj.manager_id)
            return {"id": user.id, "username": user.username, "real_name": user.real_name}
        except User.DoesNotExist:
            return None

    def validate_parent_id(self, value):
        # 新建时无 self.instance，跳过死循环校验
        if not self.instance:
            return value

        current_id = self.instance.id
        if value == current_id:
            raise serializers.ValidationError("上级部门不能为自身")

        # 死循环检测：向上递归 parent_id，看是否出现自身
        def is_cyclic(pid):
            while pid:
                if pid == current_id:
                    return True
                try:
                    parent = Department.objects.get(id=pid)
                    pid = parent.parent_id
                except Department.DoesNotExist:
                    break
            return False

        if is_cyclic(value):
            raise serializers.ValidationError("上级部门不能为自身的子孙节点")

        return value
