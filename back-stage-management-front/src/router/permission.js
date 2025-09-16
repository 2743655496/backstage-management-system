import router from './index'
import store from '@/store'

export function setupAuthGuard() {
  router.beforeEach((to, from, next) => {
    const userinfo = store.state.LoginModule.userinfo
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const guestOnly = to.matched.some(record => record.meta.guestOnly)
    // const allowedRoles = to.meta.roles || []
    // 🚫 页面未注册
    if (to.matched.length === 0) {
      return next({ path: '/404' })
    }

    // 🔁 如果页面仅限游客访问，但用户已登录，则跳转首页
    if (guestOnly && userinfo && userinfo.id) {
      return next({ path: '/' })
    }

    // 🟡 页面不需要认证，直接放行
    if (!requiresAuth) {
      return next()
    }

    // 🔒 页面需要认证，但用户未登录
    if (!userinfo || !userinfo.id) {
      return next({ path: '/auth/login', query: { redirect: to.fullPath } })
    }

    // 🔐 页面需要特定角色访问（可选）
    // if (allowedRoles.length > 0 && !allowedRoles.includes(userinfo.role)) {
    //   return next({ path: '/403' })
    // }

    // ✅ 正常放行
    next()
  })
}
