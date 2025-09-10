import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import router from './router'
import store from './store'
import '@/assets/css/reset.css'
import i18n from '@/lang/index'
import { setupAuthGuard } from '@/router/permission'
setupAuthGuard();
// 从 localStorage 获取语言设置
const savedLang = localStorage.getItem('language')
if (savedLang === 'iconfont icon-yingwen') {
  i18n.locale = 'en'
} else {
  i18n.locale = 'zh'
}

Vue.config.productionTip = false


new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
