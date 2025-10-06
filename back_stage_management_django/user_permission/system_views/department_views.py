from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from user_permission.models import Department, User
from user_permission.serializers.department_serializers import DepartmentSerializer
from user_permission.serializers.user_serializers import UserSimpleSerializer
from utils.decorators import atomic_view
from utils.serializer_errors import extract_error_message
from utils.validators import strict_validate_fields


class DepartmentListView(APIView):
    def get(self, request):
        def build_tree_with_serializer(dept_list, parent_id=0):
            """使用序列化器构建树形结构"""
            children = []
            for dept in dept_list:
                if dept.parent_id == parent_id:
                    # 序列化当前部门
                    dept_data = DepartmentSerializer(dept).data
                    # 递归获取子部门
                    dept_data['children'] = build_tree_with_serializer(dept_list, dept.id)
                    children.append(dept_data)

            # 按 sort 字段排序
            return sorted(children, key=lambda x: x['sort'])

        # 一次性获取所有部门，避免N+1查询
        departments = Department.objects.filter(is_deleted=0).select_related()
        tree_data = build_tree_with_serializer(departments)
        return Response({"data": tree_data})


class DepartmentCreateView(APIView):
    @atomic_view
    def post(self, request):
        schema = {
            "name": {"type": str, "required": True, "allow_blank": False},
            "code": {"type": str, "required": True, "allow_blank": False},
            "sort": {"type": int, "required": True},
            "status": {"type": int, "required": True, "choices": [0, 1]},
            "parent_id": {"type": int, "required": False},
            "manager_id": {"type": (int, type(None)), "required": False},
            "description": {"type": str, "required": True, "allow_blank": True},
        }

        error_response = strict_validate_fields(request.data, schema)
        if error_response:
            return error_response

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            if Department.objects.filter(name=serializer.validated_data["name"], is_deleted=0).exists():
                return Response({"message": "部门名称已存在"}, status=status.HTTP_400_BAD_REQUEST)
            if Department.objects.filter(code=serializer.validated_data["code"], is_deleted=0).exists():
                return Response({"message": "部门编码已存在"}, status=status.HTTP_400_BAD_REQUEST)
                # 🔒 禁止设置已删除部门为上级
            parent_id = serializer.validated_data.get("parent_id")
            if parent_id:
                try:
                    parent = Department.objects.get(id=parent_id)
                    if parent.is_deleted:
                        return Response({"message": "上级部门已被删除，无法设置"},
                                        status=status.HTTP_400_BAD_REQUEST)
                except Department.DoesNotExist:
                    return Response({"message": "上级部门不存在"}, status=status.HTTP_400_BAD_REQUEST)

            dept = serializer.save(creator_id=request.my_user.id)
            return Response({"message": "部门创建成功", "department_id": dept.id}, status=status.HTTP_201_CREATED)
        message = extract_error_message(serializer.errors)
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentUpdateView(APIView):
    @atomic_view
    def post(self, request, dept_id):
        # ✅ 前置字段完整性校验
        schema = {
            "name": {"type": str, "required": True, "allow_blank": False},
            "code": {"type": str, "required": True, "allow_blank": False},
            "sort": {"type": int, "required": True},
            "status": {"type": int, "required": True, "choices": [0, 1]},
            "manager_id": {"type": (int, type(None)), "required": False},
            "description": {"type": str, "required": True, "allow_blank": True},
        }

        error_response = strict_validate_fields(request.data, schema)
        if error_response:
            return error_response

        try:
            dept = Department.objects.get(id=dept_id, is_deleted=0)
        except Department.DoesNotExist:
            return Response({"error": "部门不存在"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ 禁用前检查是否有员工
        if request.data.get("status") == 0:
            def get_descendants(dept):
                descendants = []
                children = Department.objects.filter(parent_id=dept.id, is_deleted=0)
                for child in children:
                    descendants.append(child)
                    descendants.extend(get_descendants(child))
                return descendants

            all_depts = [dept] + get_descendants(dept)
            dept_ids = [d.id for d in all_depts]

            has_users = User.objects.filter(department_id__in=dept_ids, is_deleted=0).exists()
            if has_users:
                return Response({"message": "该部门及其子部门下存在员工，无法禁用"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 唯一性校验
        if "name" in request.data and Department.objects.filter(name=request.data["name"], is_deleted=0).exclude(
                id=dept_id).exists():
            return Response({"message": "部门名称已存在"}, status=status.HTTP_400_BAD_REQUEST)
        if "code" in request.data and Department.objects.filter(code=request.data["code"], is_deleted=0).exclude(
                id=dept_id).exists():
            return Response({"message": "部门编码已存在"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 更新
        serializer = DepartmentSerializer(dept, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(update_time=timezone.now())
            return Response({"message": "部门更新成功"})
        message = extract_error_message(serializer.errors)
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDeleteView(APIView):
    @atomic_view
    def post(self, request, dept_id):
        try:
            root_dept = Department.objects.get(id=dept_id, is_deleted=0)
        except Department.DoesNotExist:
            return Response({"message": "部门不存在"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ 递归获取所有子部门
        def get_descendants(dept):
            descendants = []
            children = Department.objects.filter(parent_id=dept.id, is_deleted=0)
            for child in children:
                descendants.append(child)
                descendants.extend(get_descendants(child))
            return descendants

        all_depts = [root_dept] + get_descendants(root_dept)
        dept_ids = [d.id for d in all_depts]

        # ✅ 检查是否有员工属于这些部门
        has_users = User.objects.filter(department_id__in=dept_ids, is_deleted=0).exists()
        if has_users:
            return Response({"message": "该部门或子部门下存在员工，无法删除"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 执行逻辑删除
        Department.objects.filter(id__in=dept_ids).update(is_deleted=1, update_time=timezone.now())
        return Response({"message": "部门及其子部门已删除"})


class ActiveUserListAPIView(APIView):
    """部门负责人列表获取"""

    def get(self, request):
        users = User.objects.filter(status=1, is_deleted=0)
        serializer = UserSimpleSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
