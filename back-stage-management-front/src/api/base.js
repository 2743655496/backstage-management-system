const api = {
    baseUrl:"https://192.168.18.67:8000/",//域名
    goodslist:'/api/projectList',//商品列表
    searchList:"/api/search",//搜索
    login:"/api/login/",//登录,
    checklogin:"/api/status/",//检查登录状态,
    slider_verify:"/api/slider_verify/", //滑块验证接口
    token_refresh:"/api/refresh/", //token刷新
    logout:"/api/logout/", //退出登录
}

export default api;