const api = {
    baseUrl: "https://192.168.18.67:8000/",//域名
    goodslist: '/api/user/projectList',//商品列表
    searchList: "/api/user/search",//搜索
    login: "/api/user/login/",//登录,
    checklogin: "/api/user/status/",//检查登录状态,
    slider_verify: "/api/user/slider_verify/", //滑块验证接口
    token_refresh: "/api/user/refresh/", //token刷新
    logout: "/api/user/logout/", //退出登录
    get_permission: "/api/user/permission/", //退出登录
}

export default api;