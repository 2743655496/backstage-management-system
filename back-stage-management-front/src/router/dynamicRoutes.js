// src/router/dynamicRoutes.js
import router from '@/router'
import { componentMap } from './componentMap'
import { checkAuth } from "@/utils/auth";

export function registerDynamicRoutes(menuList) {
  const layoutRoute = {
    path: '/dashboard/analysis',
    component: componentMap['Layout'],
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
        checkAuth()
        next()
      },
    children: []
  }
  menuList.forEach(menu => {
    if (componentMap[menu.component]) {
      layoutRoute.children.push({
        path: menu.path,
        name: menu.name,
        component: componentMap[menu.component],
        meta: menu.meta || {}
      })
    }
  })
  router.addRoute(layoutRoute)
}
