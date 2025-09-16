import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login/MyLogin'
import Layout from '@/views/Layout/Layout'
import Home from '@/views/Home/Home'

//异步
// 登录页面
const LoginForm = () => import('@/views/Login/LoginForm')
const ForgetPassword = () => import('@/views/Login/ForgetPassword')
const MobileLogin = () => import('@/views/Login/MobileLogin')
const QrCodeLogin = () => import('@/views/Login/QrCodeLogin')
const CreateAccount = () => import('@/views/Login/CreateAccount')
// 内容页面
const Goods = () => import('@/views/Goods/Goods')
const AddGoods = () => import('@/views/Goods/AddGoods')
const Advert = () => import('@/views/Advert/Advert')
const Order = () => import('@/views/Order/Order')
const Params = () => import('@/views/Params/Params')
const Category = () => import('@/views/Params/Category')
const User = () => import('@/views/User/User')


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    //路由元信息,配置给父组件，就会拦截下面的所有组件
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '/',
        name: "Home",
        component: Home
      },
      {
        path: '/goods',
        name: "Goods",
        component: Goods
      }, {
        path: '/add-goods',
        name: 'AddGoods',
        component: AddGoods
      },
      {
        path: '/advert',
        name: "Advert",
        component: Advert
      },
      {
        path: '/order',
        name: "Order",
        component: Order
      },
      {
        path: '/params',
        name: "Params",
        component: Params
      },
      {
        path: '/category',
        name: "Category",
        component: Category
      },
      {
        path: '/user',
        name: "User",
        component: User
      },
    ]
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
        component: LoginForm
      },
      {
        path: '/auth/create',
        name: "CreateAccount",
        component: CreateAccount
      },
      {
        path: '/auth/forget',
        name: "ForgetPassword",
        component: ForgetPassword
      },
      {
        path: '/auth/mobile_login',
        name: "MobileLogin",
        component: MobileLogin
      },
      {
        path: '/auth/qr_code',
        name: "QrCode",
        component: QrCodeLogin
      }
    ]
  },
  {
    path: '/about',
    name: 'about',
    meta: {
      requiresAuth: true
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Test.vue')
  },
  {
  path: '/:pathMatch(.*)*',
  name: 'NotFound',
  component: () => import('@/views/ErrorPages/NotFound.vue')
  },

  
]


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


export default router
