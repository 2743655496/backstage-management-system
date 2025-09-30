import { checkAuthStatus } from '@/api/modules/login';
export default {
  namespaced: true,
  state: {
    isAuthenticated: false,
    user: null,
    accessExpiresIn: null,
    refreshExpiresIn: null,
    isRefreshExpiringSoon: false,
    ip: '',
    device: ''
  },
  mutations: {
    setSession(state, payload) {
      state.isAuthenticated = payload.isAuthenticated;
      state.user = payload.user;
      state.accessExpiresIn = payload.accessExpiresIn;
      state.refreshExpiresIn = payload.refreshExpiresIn;
      state.isRefreshExpiringSoon = payload.isRefreshExpiringSoon;
      state.ip = payload.ip;
      state.device = payload.device;
    },
    clearSession(state) {
      state.isAuthenticated = false;
      state.user = null;
      state.accessExpiresIn = null;
      state.refreshExpiresIn = null;
      state.isRefreshExpiringSoon = false;
      state.ip = '';
      state.device = '';
    }
  },
  actions: {
    async pingSession({ commit }) {
      try {
        const res = await checkAuthStatus();
        const data = res.data;
        if (!data || !data.is_authenticated) {
        commit("clearSession");
        return false;
        }

        commit("setSession", {
        isAuthenticated: data.is_authenticated,
        user: data.user,
        accessExpiresIn: data.access_expires_in,
        refreshExpiresIn: data.refresh_expires_in,
        isRefreshExpiringSoon: data.is_refresh_expiring_soon,
        ip: data.ip,
        device: data.device
        });


        return true;
      } catch (err) {
        commit("clearSession");
        return false;
      }
    }
  },
  getters: {
    username: state => state.user?.username || '',
    isExpiringSoon: state => state.isRefreshExpiringSoon,
    remainingAccessTime: state => state.accessExpiresIn,
    remainingRefreshTime: state => state.refreshExpiresIn
  }
};
