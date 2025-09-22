/**
 * 所有的请求函数
 */
import ajax from "./ajax"
import base from "./base"
import qs from 'qs'; 

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
export const checkAuthStatus = () => {
  return ajax.get(base.checklogin);
}

/**
 * 退出登录
 */
export const toLogout = () => {
  return ajax.post(base.logout);
}

/**
 * 获取权限信息
 */
export const toGetPermission = () => {
  return ajax.get(base.get_permission);
}


