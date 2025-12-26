// store/modules/LightModule.js
const state = {
  isLightOn: true // 默认开灯
}

const getters = {
  isLightOn: (state) => state.isLightOn
}

const mutations = {
  SET_LIGHT_STATE(state, payload) {
    state.isLightOn = payload
  },
  TOGGLE_LIGHT(state) {
    state.isLightOn = !state.isLightOn
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
