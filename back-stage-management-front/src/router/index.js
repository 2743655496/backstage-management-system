import Vue from 'vue'
import VueRouter from 'vue-router'
import { checkAuth } from "@/utils/auth";
import Login from '@/views/Login/MyLogin'

Vue.use(VueRouter)

// 基础路由（不需要权限）
const baseRoutes = [
  {
    path: '/',
    redirect: '/dashboard/analysis'
  },

  {
    path: '/auth/login',
    name: 'Auth',
    component: Login,
    meta: { guestOnly: true },
    children: [
      {
        path: '/auth/login',
        name: "Login",
        component: () => import('@/views/Login/LoginForm.vue')
      },
      {
        path: '/auth/create',
        name: "CreateAccount",
        component: () => import('@/views/Login/CreateAccount.vue')
      },
      {
        path: '/auth/forget',
        name: "ForgetPassword",
        component: () => import('@/views/Login/ForgetPassword.vue')
      },
      {
        path: '/auth/mobile_login',
        name: "MobileLogin",
        component: () => import('@/views/Login/MobileLogin.vue')
      },
      {
        path: '/auth/qr_code',
        name: "QrCode",
        component: () => import('@/views/Login/QrCodeLogin.vue')
      },

    ]
  },
  {
    path: '/404',
    name: 'NotFound',
    meta: { requiresAuth: true },
    component: () => import('@/views/ErrorPages/NotFound.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/Test.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: baseRoutes
})

export default router
