import Vue from 'vue'
import Vuex from 'vuex'
import LoginModule from './modules/LoginModule'
import MenuStateModule from './modules/MenuState'
import LanguageModule from './modules/LanguageModule'
import createPersistedState from 'vuex-persistedstate'

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
  },
  plugins: [
    createPersistedState({
      paths: ['MenuStateModule'], // 只持久化标签页模块
      storage: window.localStorage // 使用sessionStorage（可选：换成localStorage可长期保存）
    })
  ]
})
