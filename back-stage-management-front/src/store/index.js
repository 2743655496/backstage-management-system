import Vue from 'vue'
import Vuex from 'vuex'
import LoginModule from './modules/LoginModule'
import MenuStateModule from './modules/MenuState'
import LanguageModule from './modules/LanguageModule'
import LockModule from './modules/Lock'
import PermissionModule from './modules/PermissionModule'
import chartRenderKey from './modules/chartRenderKey';
import createPersistedState from 'vuex-persistedstate'
import SessionModule from './modules/SessionModule';
import LightModule from './modules/LightModule'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    LoginModule,
    MenuStateModule,
    LanguageModule,
    LockModule,
    PermissionModule,
    chartRenderKey,
    SessionModule,
    LightModule
  },
  plugins: [
    createPersistedState({
      paths: ['MenuStateModule',
        'LockModule.isLocked',
        'LockModule.LockPassword', 'PermissionModule', 'LightModule'], // 持久化
      storage: window.localStorage // 使用sessionStorage（可选：换成localStorage可长期保存）
    })
  ]
})
