import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import router from './router'
import '@/assets/css/reset.css'
import "@/assets/iconfont/iconfont.css";
import '@/assets/iconfont/iconfont.js'
import store from '@/store'
import { registerDynamicRoutes } from '@/router/dynamicRoutes'
import i18n from '@/lang/index'
import { setupAuthGuard } from '@/router/permission'
const menusList = store.getters['PermissionModule/menusList']
if (menusList && menusList.length > 0) {
  store.dispatch("PermissionModule/fetchPermissions")
  registerDynamicRoutes(menusList)
}
setupAuthGuard();
// 从 localStorage 获取语言设置
const savedLang = localStorage.getItem('language')
if (savedLang === 'iconfont icon-yingwen') {
  i18n.locale = 'en'
} else {
  i18n.locale = 'zh'
}


new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
