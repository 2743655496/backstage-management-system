import Vue from 'vue'
import VueRouter from 'vue-router'
import Login  from '@/views/Login/Login'
import Layout from '@/views/Layout/Layout'
import Home from '@/views/Home/Home'

//异步
const Goods=()=>import('@/views/Goods/Goods')
const Advert=()=>import('@/views/Advert/Advert')
const Order=()=>import('@/views/Order/Order')
const Params=()=>import('@/views/Params/Params')
const User=()=>import('@/views/User/User')




Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    children:[
      {
        path:'/',
        name:"Home",
        component: Home
      },
      {
        path:'/goods',
        name:"Goods",
        component: Goods
      },
      {
        path:'/advert',
        name:"Advert",
        component: Advert
      },
      {
        path:'/order',
        name:"Order",
        component: Order
      },
      {
        path:'/params',
        name:"Params",
        component: Params
      },
      {
        path:'/user',
        name:"User",
        component: User
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
