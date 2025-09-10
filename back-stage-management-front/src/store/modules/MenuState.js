// MenuStateModule.js
const MenuStateModule = {
  namespaced: true,
  state: {
    CurrentMenu: [],  // 当前选中菜单
    TabMenu: []       // 标签页菜单数组
  },
  mutations: {
    // 设置当前菜单
    SET_CURRENT_MENU(state, { menu, index }) {
      // 确保 CurrentMenu 是数组
      if (!Array.isArray(state.CurrentMenu)) {
        state.CurrentMenu = []
      }
      if (menu.children && menu.children.length !== 0) {
        // 清空当前菜单，然后添加新菜单
        state.CurrentMenu = [menu, menu.children[index]]
      } else {
        // 如果没有子菜单，只添加当前菜单
        state.CurrentMenu = [menu]
      }
    },

    // 添加标签页菜单
    ADD_TAB_MENU(state, { menu, index }) {
      // 检查是否已存在
      let tabindex = null; // 使用 let 而不是 const

      if (menu.children && menu.children.length !== 0) {
        tabindex = state.TabMenu.findIndex(item => item.router_path === menu.children[index].router_path);
        if (tabindex === -1) {
          state.TabMenu.push(menu.children[index])
        }
      } else {
        // 检查当前菜单项是否已存在
        tabindex = state.TabMenu.findIndex(item => item.router_path === menu.router_path);
        if (tabindex === -1) {
          state.TabMenu.push(menu)
        }
      }
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
    }
  },
  actions: {
    // 异步设置当前菜单
    setCurrentMenu({ commit }, [menu, index]) {
      commit('SET_CURRENT_MENU', { menu, index })
      // 自动添加到标签页
      commit('ADD_TAB_MENU', { menu, index })
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