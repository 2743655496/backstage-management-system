# ① 完全公开接口（无需登录、无需权限）
PUBLIC_WHITELIST = {
    "/api/system/auth/login": ["POST"],
    "/api/system/auth/slider_verify": ["POST"],
    "/api/system/auth/refresh": ["POST"],
}

# ② 登录即可访问（无需权限）
LOGIN_ONLY_WHITELIST = {
    "/api/system/auth/status": ["GET"],
    "/api/system/auth/permission": ["GET"],
    "/api/system/permissions": ["GET"],
    "/api/system/departments": ["GET"],
    "/api/system/menus": ["GET"],
    "/api/system/roles": ["GET"],
    "/api/system/departments/principal": ["GET"],
}

# ③ 动态路径白名单（需要登录，但无需权限）
LOGIN_ONLY_PREFIX = {
    "/api/system/roles/detail_update": ["GET"],  # 例如动态路径
    "/api/system/users/detail_update": ["GET"],  # 例如动态路径
}
