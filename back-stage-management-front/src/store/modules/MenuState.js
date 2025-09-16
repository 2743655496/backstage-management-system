import { resolveMenuPath } from '@/utils/menuResolver'
// MenuStateModule.js
const MenuStateModule = {
  namespaced: true,
  state: {
    CurrentMenu: [],  // 当前选中菜单
    TabMenu: []       // 标签页菜单数组
  },
  mutations: {
    // 设置当前菜单
    SET_CURRENT_MENU(state, menus) {
      // 确保 CurrentMenu 是数组
      state.CurrentMenu = menus
    },

    // 添加标签页菜单
    ADD_TAB_MENU(state, menu) {

      const exists = state.TabMenu.some(item => item.path === menu.path)
      if (!exists) {
        state.TabMenu.push(menu)
      }

      // 排序：固定标签在前
      const fixedTags = state.TabMenu.filter(t => t.fixed)
      const normalTags = state.TabMenu.filter(t => !t.fixed)
      state.TabMenu = [...fixedTags, ...normalTags]
    },

    // 删除标签页菜单
    REMOVE_TAB_MENU(state, path) {
      state.TabMenu = state.TabMenu.filter(item => item.path !== path)
    },

    // 清空标签页
    CLEAR_TAB_MENU(state) {
      state.TabMenu = []
    },

    //清楚当前选中菜单
    CLEAR_CURRENT_MENU(state) {
      state.CurrentMenu = []
    },

    // 固定或取消固定标签页
    TOGGLE_FIXED_TAB_MENU(state, path) {
      const index = state.TabMenu.findIndex(item => item.path === path)
      if (index !== -1) {
        const tag = state.TabMenu[index]
        tag.fixed = !tag.fixed
        // 重新排序：固定的放前面
        const fixedTags = state.TabMenu.filter(t => t.fixed)
        const normalTags = state.TabMenu.filter(t => !t.fixed)
        state.TabMenu = [...fixedTags, ...normalTags]
      }

    },
    CLEAR_ALL_MENUS(state) {
      state.CurrentMenu = []
      state.TabMenu = []
    }

  },
  actions: {
    // 异步设置当前菜单
    setCurrentMenuaddTabMenu({ commit, rootGetters }, path) {
      const menus = rootGetters['PermissionModule/menuPermissions']
      const result = resolveMenuPath(menus, path)
      commit('SET_CURRENT_MENU', result.currentMenu)
      // 自动添加到标签页
      commit('ADD_TAB_MENU', result.tabMenu)
    },

    // 添加标签页
    addTabMenu({ commit }, menu) {
      commit('ADD_TAB_MENU', menu)
    },

    // 删除标签页
    removeTabMenu({ commit, state }, path) {
      commit('REMOVE_TAB_MENU', path)

      // 如果删除的是当前菜单，则设置第一个标签为当前菜单
      if (state.CurrentMenu.path === path && state.TabMenu.length > 0) {
        commit('SET_CURRENT_MENU', state.TabMenu[0])
      }
    },

    // 清空标签页
    clearTabMenu({ commit }) {
      commit('CLEAR_TAB_MENU')
    },

    // 切换标签页固定状态
    toggleFixedTabMenu({ commit }, path) {
      commit('TOGGLE_FIXED_TAB_MENU', path)
    },

    clearAllMenus({ commit }) {
      commit('CLEAR_ALL_MENUS')
    }
  },
  getters: {
    // 获取当前菜单
    currentMenu: state => state.CurrentMenu,

    // 获取标签页菜单
    tabMenus: state => state.TabMenu,

    // 检查菜单是否在标签页中
    hasTabMenu: state => path => {
      return state.TabMenu.some(item => item.path === path)
    }
  }
}

export default MenuStateModule