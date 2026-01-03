import axios from "axios";
import base from "./base";
import router from "@/router/index";
import { Message } from 'element-ui';
import store from '@/store';

let isRefreshing = false;
let requestsQueue = [];
let hasLoggedOut = false; // ✅ 防止重复登出提示和跳转

const service = axios.create({
  baseURL: base.baseUrl,
  timeout: 5000,
  withCredentials: true // ✅ 自动携带 HttpOnly Cookie
});

// 请求拦截器（无需手动加 token）
service.interceptors.request.use(
  config => config,
  error => Promise.reject(error)
);

// 响应拦截器
service.interceptors.response.use(
  res => res,
  async error => {
    const { response, config } = error;

    if (!response) {
      Message.error('网络连接失败，请检查您的网络设置');
      error.__handled = true;
      return Promise.reject(error);
    }

    // 🔑 401 未授权
    if (response.status === 401) {
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const url = new URL(base.token_refresh, base.baseUrl).toString();
          const res = await axios.post(url, {}, { withCredentials: true });
          if (res.data.code === 200) {
            requestsQueue.forEach(cb => cb());
            requestsQueue = [];
            return service(config);
          } else {
            clearRequestQueue();
            handleLogout();
            return Promise.reject('未登录或登录已过期');
          }
        } catch (e) {
          clearRequestQueue();
          handleLogout();
          return Promise.reject(e);
        } finally {
          isRefreshing = false;
        }
      } else {
        return new Promise(resolve => {
          requestsQueue.push(() => resolve(service(config)));
        });
      }
    }

    // 🚫 403 权限不足（你新增的逻辑）
    if (response.status === 403) {
      const msg = response?.data?.detail || response?.data?.message || '您没有权限执行此操作';
      Message.error(msg);
      error.__handled = true;
      return Promise.reject(error);
    }

    // ⚠️ 400 参数错误
    if (response.status === 400) {
      const msg = response?.data?.message || '请求参数错误，请检查';
      Message.error(msg);
      error.__handled = true;
    }

    // 🚫 404 资源未找到
    if (response.status === 404) {
      const msg = response?.data?.message || '请求的资源不存在';
      Message.error(msg);
      error.__handled = true;
    }

    // 🔥 500 服务器错误
    if (response.status === 500) {
      const msg = response?.data?.message || '服务器内部错误，请稍后再试';
      Message.error(msg);
      error.__handled = true;
    }

    // ⏱️ 请求超时
    if (error.code === 'ECONNABORTED') {
      Message.error('请求超时，请稍后重试');
      error.__handled = true;
    }

    // 📦 其他错误（排除 401，避免重复提示）
    if (![400, 401, 403, 404, 500].includes(response.status)) {
      const msg = response?.data?.message || '请求失败，请稍后再试';
      Message.error(msg);
      error.__handled = true;
    }

    return Promise.reject(error);
  }
);


// ✅ 清空挂起请求队列
function clearRequestQueue() {
  requestsQueue = [];
}

// ✅ 统一登出处理（防止重复执行）
function handleLogout() {
  if (hasLoggedOut) return;
  hasLoggedOut = true;
  store.commit('LoginModule/clearUser');
  store.dispatch('PermissionModule/clearPermissions');
  store.dispatch('MenuStateModule/clearAllMenus');
  store.dispatch('LockModule/clearLock');
  Message.error('未登录或登录已过期');
  router.push({ name: 'Login' });
}

// ✅ 登录成功后建议调用此方法重置登出标志
export function resetLogoutFlag() {
  hasLoggedOut = false;
}

export default service;
