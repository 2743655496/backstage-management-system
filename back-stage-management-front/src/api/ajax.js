import axios from "axios";
import base from "./base";
import router from "@/router/index";
import { Message } from 'element-ui';
import store from '@/store'


const service = axios.create({
    baseURL: base.baseUrl,
    timeout: 5000,
    withCredentials: true // ✅ 发送 Cookie（access_token / refresh_token）
})

//请求拦截
service.interceptors.request.use(config => {
    return config
})

//响应拦截
service.interceptors.response.use(res => {
    return res
}, async error => {
    // 🌐 网络错误（断网、DNS错误等）
    if (!error.response) {
        Message.error('网络连接失败，请检查您的网络设置')
    }

    else if (error.response && error.response.status === 401) {
        const res = await service.post(base.token_refresh);
        if (res.data.code != 200) {
            // 清除 Vuex 中的用户信息
            store.commit('LoginModule/clearUser');
            store.commit('PermissionModule/clearPermissions');
            store.commit('MenuStateModule/clearAllMenus');
            store.commit('LockModule/clearLock');
            Message({
                showClose: true,
                message: '未登录或登录已过期',
                type: 'error'
            });
            router.push({ name: 'Login' });
        }
    }
    // 🔥 500 服务器错误
    else if (error.response && error.response.status === 500) {
        Message.error('服务器内部错误，请稍后再试')
    }

    // ⏱️ 请求超时
    else if (error.code === 'ECONNABORTED') {
        Message.error('请求超时，请稍后重试')
    }

    // 📦 其他错误
    else {
        const msg = error.response?.data?.message || '请求失败，请稍后再试'
        Message.error(msg)
    }
    return Promise.reject(error)
})

export default service;