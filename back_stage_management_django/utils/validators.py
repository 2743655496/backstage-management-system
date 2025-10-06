from rest_framework.response import Response
from rest_framework import status

def strict_validate_fields(data: dict, schema: dict):
    """
    严格字段校验器：用于在视图层对 request.data 进行结构和字段合法性校验。

    ✅ 功能特点：
    - 固定字段白名单：只允许 schema 中定义的字段，多传即报错
    - 支持字段缺失校验：required=True 时字段必须存在且不能为 None
    - 支持类型校验：type 可为单类型或类型元组，如 int、(int, type(None))
    - 支持空字符串校验：仅对 str 类型字段生效，allow_blank 控制是否允许 ""
    - 支持枚举值校验：choices 限定字段值必须在指定列表中

    ✅ 参数说明：
    :param data: dict
        请求体数据，一般为 request.data

    :param schema: dict
        字段规则定义，格式如下：
        {
            "字段名": {
                "required": bool,         # 是否必填
                "type": type 或 (type1, type2),  # 期望类型
                "allow_blank": bool,      # 是否允许空字符串，仅对 str 类型有效
                "choices": list           # 枚举值列表，字段值必须在其中
            }
        }

    ✅ 返回值：
    - 如果校验通过，返回 None
    - 如果校验失败，返回 Response 对象（HTTP 400），包含 message 字段说明错误原因

    ✅ 示例 schema：
    schema = {
        "name": {"type": str, "required": True, "allow_blank": False},
        "code": {"type": str, "required": True, "allow_blank": False},
        "sort": {"type": int, "required": True},
        "status": {"type": int, "required": True, "choices": [0, 1]},
        "parent_id": {"type": int, "required": False},
        "manager_id": {"type": (int, type(None)), "required": False},
        "description": {"type": str, "required": True, "allow_blank": True},
    }

    ✅ 示例调用：
    error_response = strict_validate_fields(request.data, schema)
    if error_response:
        return error_response

    ✅ 错误提示示例：
    - {"message": "缺少必要参数：name"}
    - {"message": "存在未定义字段：creator_id"}
    - {"message": "status取值无效，应为：0, 1"}
    - {"message": "manager_id类型错误，应为：int, NoneType"}
    - {"message": "code不能为空"}

    ✅ 推荐使用场景：
    - 接口入口前置防御，防止非法字段进入序列化器
    - 替代 DRF 默认错误提示，提供更友好的中文反馈
    - 与事务装饰器、日志记录器组合使用，构建企业级视图逻辑

    ✅ 扩展建议：
    - 支持默认值填充：default
    - 支持字段别名映射：alias
    - 支持嵌套字段校验：user.real_name
    - 支持字段值转换：cast（如 str → int）

    """
    # ✅ 检查是否有多余字段
    unexpected_fields = [field for field in data if field not in schema]
    if unexpected_fields:
        return Response(
            {"message": f"存在未定义字段：{', '.join(unexpected_fields)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ 遍历 schema 做字段校验
    for field, rules in schema.items():
        value = data.get(field)

        # ✅ 必填字段缺失 或 值为 None
        if rules.get("required", False):
            if field not in data:
                return Response({"message": f"缺少必要参数：{field}"}, status=status.HTTP_400_BAD_REQUEST)
            if value is None:
                return Response({"message": f"{field}不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 空字符串校验（仅针对 str）
        if isinstance(value, str) and not rules.get("allow_blank", True):
            if value.strip() == "":
                return Response({"message": f"{field}不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 类型校验（跳过 None，只在 required=False 时允许）
        expected_type = rules.get("type")
        if expected_type and value is not None and not isinstance(value, expected_type):
            if not isinstance(expected_type, tuple):
                expected_type = (expected_type,)
            expected_names = ", ".join([t.__name__ for t in expected_type])
            return Response({"message": f"{field}类型错误，应为：{expected_names}"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 枚举值校验
        choices = rules.get("choices")
        if choices and value not in choices:
            return Response({"message": f"{field}取值无效，应为：{', '.join(map(str, choices))}"}, status=status.HTTP_400_BAD_REQUEST)

    return None
