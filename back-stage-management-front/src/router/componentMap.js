export const componentMap = {
  // 'Home': () => import('@/views/Home/Home.vue'),
  // 'Goods': () => import('@/views/Goods/Goods.vue'),
  // 'AddGoods': () => import('@/views/Goods/AddGoods.vue'),
  // 'Advert': () => import('@/views/Advert/Advert.vue'),
  // 'Order': () => import('@/views/Order/Order.vue'),
  // 'Params': () => import('@/views/Params/Params.vue'),
  // 'Category': () => import('@/views/Params/Category.vue'),
  // 'User': () => import('@/views/User/User.vue'),
  // 'Test': () => import('@/views/Test.vue'),
  'Layout': () => import('@/views/Layout/Layout.vue'),
  // 概览
  'dashboard/workbench': () => import('@/views/Overview/Workbench.vue'),
  'dashboard/analysis': () => import('@/views/Overview/Dashboard.vue'),
  // 系统管理
  'system/role': () => import('@/views/System/Role.vue'),
  'system/department': () => import('@/views/System/Department.vue'),
  'system/user': () => import('@/views/System/User.vue'),
  'system/permission': () => import('@/views/System/Permission.vue'),
  'system/menu': () => import('@/views/System/MenuManagement.vue'),
}
