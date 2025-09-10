import router from "./index";
import store from '@/store'
// import { Loading } from 'element-ui'



// 路由守卫主函数
export function setupAuthGuard() {
  // let loadingInstance = null
  router.beforeEach((to, from, next) => {
    // 显示加载动画
    // loadingInstance = Loading.service({
    //   lock: true,
    //   text: '页面加载中...',
    //   spinner: 'el-icon-loading',
    //   background: 'rgba(0, 0, 0, 0.3)'
    // })
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const isGuestOnly = to.matched.some(record => record.meta.guestOnly)

    const userinfo = store.state.LoginModule.userinfo // 假设模块名为 LoginModule
    const isLoggedIn = !!userinfo && !!userinfo.id // 判断是否登录

    if (requiresAuth) {
      // 需要登录的页面
      if (isLoggedIn) {
        next() // 已登录，放行
      } else {
        next({
          path: '/auth/login',
          query: { redirect: to.fullPath } // 登录后跳回原页面
        })
      }
    } else if (isGuestOnly) {
      // 仅限未登录访问的页面（如登录页）
      if (isLoggedIn) {
        next({ path: '/' }) // 已登录，不允许访问登录页，跳转首页
      } else {
        next() // 未登录，放行
      }
    } else {
      // 普通页面，无需登录
      next()
    }
  })


//   router.afterEach(() => {
  //   // 关闭加载动画
  //   if (loadingInstance) {
  //     loadingInstance.close()
  //   }
  // })

  //路由拦截(废弃方案影响速度)
  // router.beforeEach(async (to, from, next) => {
  //   const requiresAuth = to.matched.some(record => record.meta.requiresAuth); // 👈 自定义字段，标记需要登录的页面
  //   const isGuestOnly = to.matched.some(record => record.meta.guestOnly);

  //   // ✅ 如果带有 skipAuthCheck 参数，直接放行

  //   if (isGuestOnly && to.params.skipAuthCheck === 'true') {
  //     return next();
  //   } else {
  //     try {

  //       const res = await checkAuthStatus();
  //       const isAuthenticated = res.data.is_authenticated;

  //       if (isGuestOnly && isAuthenticated) {
  //         return next('/'); // 已登录访问访客页，跳转首页
  //       }

  //       if (!requiresAuth) {
  //         return next(); // 不需要登录，直接放行
  //       }

  //       if (isAuthenticated) {
  //         store.commit('LoginModule/setUserInfo', res.data.user);
  //         return next();
  //       } else {
  //         return next('/auth/login');
  //       }
  //     } catch (err) {
  //       // if (isGuestOnly) {
  //       // return next(); // 访客页放行
  //       // } else {
  //       //   return next('/auth/login'); // 受保护页跳转
  //       // }
  //       if (!err.response) {
  //         // 没有 response，说明请求根本没发出去或服务器无响应
  //         router.push('/auth/login')
  //       }
  //     }
  //   }
  // });
}








