/**
 * 所有的请求函数
 */
import ajax from "./ajax"
import base from "./base"
import qs from 'qs'; // 确保这一行存在
/**
 * 查询商品列表
 * params:{page:}
 */

export const getGoodsList = () => ajax.get(base.goodslist, { params })

/**
 * 查询搜素列表
 * get传参方式
 * 1.字符串拼接 ？search=xxx&name=123
 * 2.params axios.get(url,{params:{search:xx}})
 * params:{search:xx}
 */
export const getSearchList = (params) => ajax.get(base.searchList, { params })



/**
 * 登录
 * 参数：username,password,slider_token,remember
 */
export const toLogin = (params) => {
    return ajax.post(base.login, params)
}

/**
 * 滑块验证接口
 * 参数：trail
 */

export const toslider_verify = (params) => {
    return ajax.post(base.slider_verify, params)
}

/**
 * 检查当前token是否失效
 */
export const checkAuthStatus= () => {
  return ajax.get(base.checklogin);
}

/**
 * 退出登录
 */
export const toLogout= () => {
  return ajax.post(base.logout);
}


