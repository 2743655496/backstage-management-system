const state = {
  isLocked: false,
  LockPassword: '',
  showSetPassword: false // 新增：控制设置密码弹窗显示
}

const mutations = {
  SET_LOCK(state, status) {
    state.isLocked = status
  },
  SET_PASSWORD(state, pwd) {
    state.LockPassword = pwd
  },
  CLEAR_LOCK(state) {
    state.isLocked = false
    state.LockPassword = ''
  },
  SET_SHOW_SET_PASSWORD(state, status) {
    state.showSetPassword = status
  }
}

const actions = {
  lock({ commit }) {
    commit('SET_LOCK', true)
  },
  unlock({ commit }) {
    commit('SET_LOCK', false)
  },
  SetLockPassword({ commit }, pwd) {
    commit('SET_PASSWORD', pwd)
  },
  clearLock({ commit }) {
    commit('CLEAR_LOCK')
  },
  setShowSetPassword({ commit }, status) {
    commit('SET_SHOW_SET_PASSWORD', status)
  }
}

const getters = {
  LockPassword: state => state.LockPassword,
  showSetPassword: state => state.showSetPassword
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
