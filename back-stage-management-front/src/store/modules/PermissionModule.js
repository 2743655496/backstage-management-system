import { toGetPermission } from '@/api/index'
import { registerDynamicRoutes } from '@/router/dynamicRoutes'


const state = {
    menusList: [],
    menuPermissions: [],
    permissionMap: {}
}

const mutations = {
    SET_MENUS_LIST(state, list) {
        state.menusList = list
    },
    SET_MENU_PERMISSIONS(state, tree) {
        state.menuPermissions = tree
    },
    SET_PERMISSION_MAP(state, map) {
        state.permissionMap = map
    },
    CLEAR_PERMISSIONS(state) {
        state.menusList = []
        state.menuPermissions = []
        state.permissionMap = {}
    }
}

const actions = {
    async fetchPermissions({ commit }) {
        try {
            const res = await toGetPermission()
            const { menus_list, menu_permissions, permission_map } = res.data

            commit('SET_MENUS_LIST', menus_list)
            commit('SET_MENU_PERMISSIONS', menu_permissions)
            commit('SET_PERMISSION_MAP', permission_map)

            // 注册动态路由
            registerDynamicRoutes(menus_list)
        } catch (error) {
            console.error('权限加载失败:', error)
        }
    },
    clearPermissions({ commit }) {
        commit('CLEAR_PERMISSIONS')
    }
}

const getters = {
    menusList: state => state.menusList,
    menuPermissions: state => state.menuPermissions,
    permissionMap: state => state.permissionMap
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}
