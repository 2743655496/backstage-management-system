// store/modules/LightModule.js
const state = {
  isLightOn: true, // 默认开灯（白天）
  backgroundColor: "white",
  textColor: "#000000",
  activeColor: "#409EFF",
  hoverColor: "#ecf5ff" // 默认白天 hover 色
}

const getters = {
  isLightOn: (state) => state.isLightOn,
  backgroundColor: (state) => state.backgroundColor,
  textColor: (state) => state.textColor,
  activeColor: (state) => state.activeColor,
  hoverColor: (state) => state.hoverColor
}

const mutations = {
  SET_LIGHT_STATE(state, payload) {
    state.isLightOn = payload
    state.backgroundColor = payload ? "white" : "#000000"
    state.textColor = payload ? "#000000" : "white"
    state.activeColor = payload ? "#409EFF" : "#66b1ff"
    state.hoverColor = payload ? "#ecf5ff" : "#242424"
  },

  TOGGLE_LIGHT(state) {
    state.isLightOn = !state.isLightOn
    state.backgroundColor = state.isLightOn ? "white" : "#000000"
    state.textColor = state.isLightOn ? "#000000" : "white"
    state.activeColor = state.isLightOn ? "#409EFF" : "#66b1ff"
    state.hoverColor = state.isLightOn ? "#ecf5ff" : "#242424"
  }
}

const actions = {
  setLightState({ commit }, payload) {
    commit('SET_LIGHT_STATE', payload)
  },
  toggleLight({ commit }) {
    commit('TOGGLE_LIGHT')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
