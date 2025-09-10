import hashlib
import os


def secure_hash_password(password, salt=None):
    """使用 SHA-256 和盐值加密密码"""
    if salt is None:
        salt = os.urandom(16).hex()  # 生成随机盐值

    # 组合密码和盐值
    salted_password = (password + salt).encode()

    # 使用 SHA-256 加密
    hashed = hashlib.sha256(salted_password).hexdigest()

    return f"{salt}${hashed}"  # 存储格式：盐值$哈希值


def verify_secure_password(input_password, stored_hash):
    """验证加密密码"""
    salt, original_hash = stored_hash.split('$')

    # 用同样的方式加密输入密码
    test_hash = hashlib.sha256((input_password + salt).encode()).hexdigest()

    return test_hash == original_hash


# # 使用示例
# password = "admin123"
# stored_hash = secure_hash_password(password)  # 存储这个值
# print(stored_hash)
# # 验证
# is_valid = verify_secure_password("admin123", stored_hash)  # True
# print(is_valid)
# is_valid = verify_secure_password("wrong_password", stored_hash)  # False
# print(is_valid)