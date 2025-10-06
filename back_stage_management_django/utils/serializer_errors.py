def extract_error_message(errors):
    """
    提取 serializer.errors 中的首条错误信息
    """
    if isinstance(errors, dict):
        for field, messages in errors.items():
            if isinstance(messages, list) and messages:
                if "This field may not be blank" in messages[0]:
                    return f"{field}:{messages[0]}"
                return f"{messages[0]}"
            elif isinstance(messages, dict):
                return extract_error_message(messages)
    return "请求参数错误，请检查"
