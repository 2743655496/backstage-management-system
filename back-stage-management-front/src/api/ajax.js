import axios from "axios";
import base from "./base";
import router from "@/router/index";
import { Message } from 'element-ui';
import store from '@/store'

let isRefreshing = false
let requestsQueue = []

const service = axios.create({
    baseURL: base.baseUrl,
    timeout: 5000,
    withCredentials: true // ✅ 自动携带 HttpOnly Cookie
})

// 请求拦截器（这里不用手动加 token）
service.interceptors.request.use(config => config, error => Promise.reject(error))

// 响应拦截器
service.interceptors.response.use(
    res => res,
    async error => {
        const { response, config } = error

        if (!response) {
            Message.error('网络连接失败，请检查您的网络设置')
            return Promise.reject(error)
        }

        // 🔑 401 未授权
        if (response.status === 401) {
            if (!isRefreshing) {
                isRefreshing = true
                try {
                    const url = new URL(base.token_refresh, base.baseUrl).toString()
                    // 调用刷新接口（后端会重新设置 Cookie）
                    const res = await axios.post(url, {}, { withCredentials: true })
                    if (res.data.code === 200) {
                        // 刷新成功：重放队列里的请求
                        requestsQueue.forEach(cb => cb())
                        requestsQueue = []

                        // 重试当前请求
                        return service(config)
                    } else {
                        handleLogout()
                        return Promise.reject('未登录或登录已过期')
                    }
                } catch (e) {
                    handleLogout()
                    return Promise.reject(e)
                } finally {
                    isRefreshing = false
                }
            } else {
                // 如果正在刷新，挂起请求，等待刷新完成
                return new Promise(resolve => {
                    requestsQueue.push(() => resolve(service(config)))
                })
            }
        }

        // 🔥 500 服务器错误
        if (response.status === 500) {
            Message.error('服务器内部错误，请稍后再试')
        }

        // ⏱️ 请求超时
        if (error.code === 'ECONNABORTED') {
            Message.error('请求超时，请稍后重试')
        }

        // 📦 其他错误
        const msg = response?.data?.message || '请求失败，请稍后再试'
        Message.error(msg)

        return Promise.reject(error)
    }
)

// 统一登出处理
function handleLogout() {
    store.commit('LoginModule/clearUser')
    store.dispatch('PermissionModule/clearPermissions')
    store.dispatch('MenuStateModule/clearAllMenus')
    store.dispatch('LockModule/clearLock')
    Message.error('未登录或登录已过期')
    router.push({ name: 'Login' })
}

export default service
