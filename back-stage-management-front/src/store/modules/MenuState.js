import { resolveMenuPath } from '@/utils/menuResolver'

const MenuStateModule = {
  namespaced: true,
  state: {
    CurrentMenu: [],  // 当前选中菜单
    TabMenu: []       // 标签页菜单数组
  },
  mutations: {
    SET_TAB_MENU(state, menus) {
      state.TabMenu = menus
    },

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
      state.TabMenu = state.TabMenu.filter(item => item.fixed)
    }
    ,

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
    // 清楚参数
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
    removeTabMenu({ state, commit, dispatch }, { path, router, if_current }) {
      const tabs = state.TabMenu
      const index = tabs.findIndex(item => item.path === path)

      let targetPath = null
      const defaultPath = '/dashboard/analysis'

      // 只在删除“当前激活标签”时才处理跳转逻辑
      if (if_current) {
        if (index > 0) {
          // 有前一个 → 跳前一个
          targetPath = tabs[index - 1].path
        } else if (index === 0 && tabs.length > 1) {
          // 没前一个但有后一个 → 跳后一个
          targetPath = tabs[1].path
        } else {
          // 只剩自己或根本没找到 → 跳默认页
          targetPath = defaultPath
        }
      }

      // 先删标签
      commit('REMOVE_TAB_MENU', path)

      // 再根据算好的 targetPath 跳转 + 同步菜单
      if (if_current && targetPath) {
        if (router.currentRoute.path !== targetPath) {
          router.push(targetPath)
        }
        dispatch('setCurrentMenuaddTabMenu', targetPath)
      }
    },


    // 清空标签页列表
    clearTabMenu({ state, commit, dispatch }, router) {
      const defaultPath = '/dashboard/analysis'

      // 1. 清除非固定标签
      commit('CLEAR_TAB_MENU')   // 内部已经 filter 只保留 fixed 标签

      const fixedTabs = state.TabMenu

      // 2. 如果没有固定标签 → 跳默认页
      if (fixedTabs.length === 0) {
        if (router.currentRoute.path !== defaultPath) {
          router.push(defaultPath)
        }
        dispatch('setCurrentMenuaddTabMenu', defaultPath)
        return
      }

      // 3. 有固定标签 → 判断当前路由是否在 fixedTabs 中
      const currentPath = router.currentRoute.path
      const existsInFixed = fixedTabs.some(t => t.path === currentPath)

      if (!existsInFixed) {
        // 当前路由不在固定标签中 → 跳第一个固定标签
        const targetPath = fixedTabs[0].path
        if (currentPath !== targetPath) {
          router.push(targetPath)
        }
        dispatch('setCurrentMenuaddTabMenu', targetPath)
      }

      // 4. 当前路由就在 fixed 标签中 → 不跳转、不操作
    },

    // 关闭其他标签页（保留当前 + fixed）
    closeOtherTabs({ state, commit, dispatch }, router) {
      const currentPath = router.currentRoute.path

      const newTabs = state.TabMenu.filter(
        t => t.fixed || t.path === currentPath
      )

      commit('SET_TAB_MENU', newTabs)

      // 当前标签必须存在，否则跳转
      const exists = newTabs.some(t => t.path === currentPath)
      if (!exists) {
        const target = newTabs[0] || { path: '/dashboard/analysis' }
        router.push(target.path)
        dispatch('setCurrentMenuaddTabMenu', target.path)
      }
    },

    // 关闭左侧标签页
    closeLeftTabs({ state, commit, dispatch }, router) {
      const currentPath = router.currentRoute.path
      const index = state.TabMenu.findIndex(t => t.path === currentPath)

      if (index === -1) return

      const newTabs = state.TabMenu.filter((t, i) =>
        t.fixed || i >= index
      )

      commit('SET_TAB_MENU', newTabs)

      dispatch('setCurrentMenuaddTabMenu', currentPath)
    },

    // 关闭右侧标签页
    closeRightTabs({ state, commit, dispatch }, router) {
      const currentPath = router.currentRoute.path
      const index = state.TabMenu.findIndex(t => t.path === currentPath)

      if (index === -1) return

      const newTabs = state.TabMenu.filter((t, i) =>
        t.fixed || i <= index
      )

      commit('SET_TAB_MENU', newTabs)

      dispatch('setCurrentMenuaddTabMenu', currentPath)
    },


    // 切换标签页固定状态
    toggleFixedTabMenu({ commit }, path) {
      commit('TOGGLE_FIXED_TAB_MENU', path)
    },

    // 参数设置为空
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