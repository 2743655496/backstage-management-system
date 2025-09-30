const api = {
    baseUrl: "https://192.168.18.67:8000/",//域名
    searchList: "/api/system/search",//搜索
    login: "/api/system/login/",//登录,
    checklogin: "/api/system/status/",//检查登录状态,
    slider_verify: "/api/system/slider_verify/", //滑块验证接口
    token_refresh: "/api/system/refresh/", //token刷新
    logout: "/api/system/logout/", //退出登录
    get_permission: "/api/system/permission/", //用户权限信息
    get_menu:"/api/system/menus/", //菜单信息列表
    add_menu:"/api/system/menus/create/",//添加菜单
    update_menu:"/api/system/menus/update/",//更新菜单
    delete_menu:"/api/system/menus/delete/",//删除菜单
    get_permissions:"/api/system/permissions/",//获取权限列表
    delete_permission:"/api/system/permissions/delete/",//删除权限
}

export default api;