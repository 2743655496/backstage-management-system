import i18n from '@/lang/index'

const state = {
  currentLanguage: localStorage.getItem("language") || "iconfont icon-zhongwen",
  languages: [
    { name: "中文", icon: "iconfont icon-zhongwen" },
    { name: "英文", icon: "iconfont icon-yingwen" }
  ]
}

const mutations = {
  SET_LANGUAGE(state, icon) {
    state.currentLanguage = icon
    localStorage.setItem("language", icon)
  }
}

const actions = {
  changeLanguage({ commit }, langName) {
    let icon = "iconfont icon-zhongwen"
    let locale = "zh"
    if (langName === "英文") {
      icon = "iconfont icon-yingwen"
      locale = "en"
    }

    commit("SET_LANGUAGE", icon)

    // 如果你在 main.js 中挂载了 vm，可以这样访问 i18n
    // if (window.vm && window.vm.$i18n) {
    //   console.log("123")
    //   window.vm.$i18n.locale = locale
    // }
    i18n.locale = locale
  }
}

const getters = {
  currentLanguage: (state) => state.currentLanguage,
  languages: (state) => state.languages
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
