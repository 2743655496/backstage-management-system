const api = {
    baseUrl: "https://192.168.18.67:8000/",//域名
    login: "/api/system/auth/login/",//登录,
    checklogin: "/api/system/auth/status/",//检查登录状态,
    slider_verify: "/api/system/auth/slider_verify/", //滑块验证接口
    token_refresh: "/api/system/auth/refresh/", //token刷新
    logout: "/api/system/auth/logout/", //退出登录
    get_permission: "/api/system/auth/permission/", //用户权限信息
    get_menu:"/api/system/menus/", //菜单信息列表
    add_menu:"/api/system/menus/create/",//添加菜单
    update_menu:"/api/system/menus/update/",//更新菜单
    delete_menu:"/api/system/menus/delete/",//删除菜单
    get_permissions:"/api/system/permissions/",//获取权限列表
    add_permission:"/api/system/permissions/create/",//添加权限
    update_permission:"/api/system/permissions/update/",//更新权限
    delete_permission:"/api/system/permissions/delete/",//删除权限
    get_departments:"/api/system/departments/",//获取部门列表
    add_department:"/api/system/departments/create/",//添加部门
    update_department:"/api/system/departments/update/",//更新部门
    delete_department:"/api/system/departments/delete/",//删除部门
    get_department_principal:"/api/system/departments/principal/",//获取部门负责人列表
    get_roles:"/api/system/roles/",//获取角色列表
    get_role_detail:"/api/system/roles/detail_update/",//获取角色详情
    add_role:"/api/system/roles/",//添加角色
    update_role:"/api/system/roles/detail_update/",//更新角色
    delete_role:"/api/system/roles/delete/",//删除角色

    get_users:"/api/system/users/",//获取用户列表
    get_user_detail:"/api/system/users/detail_update/",//获取用户详情
    add_user:"/api/system/users/",//添加用户
    update_user:"/api/system/users/detail_update/",//更新用户
    delete_user:"/api/system/users/delete/",//删除用户


}

export default api;