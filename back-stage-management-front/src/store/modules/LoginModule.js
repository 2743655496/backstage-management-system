import { toLogin, toLogout } from "@/api/modules/login.js";
import { resetLogoutFlag } from "@/api/ajax";

export default {
  namespaced: true,
  state: {
    userinfo: JSON.parse(localStorage.getItem("userinfo")) || {
      id: '',
      username: '',
      avatar: '',
      email: '',
    }
  },
  mutations: {
    setUserInfo(state, payload) {
      state.userinfo = { ...payload };
      localStorage.setItem("userinfo", JSON.stringify(state.userinfo));
    },
    clearUser(state) {
      state.userinfo = {
        id: '',
        username: '',
        avatar: '',
        email: '',
      };
      localStorage.removeItem("userinfo");
    }
  },
  actions: {
    async login({ commit, dispatch }, { loginData, router, message }) {
      try {
        const res = await toLogin(loginData);
        const user = res.data.user;
        commit("setUserInfo", user);
        resetLogoutFlag(); // ✅ 重置登出标志
        message?.success("登录成功");

        await dispatch("PermissionModule/fetchPermissions", null, { root: true });

        setTimeout(() => {
          router.push("/");
        }, 100);
      } catch (error) {

        if (!error.__handled) {
          message?.error("登录失败，请检查用户名和密码");
        }
        throw error; // ✅ 抛出错误让组件 catch 到
      }
    },

    logout({ commit, dispatch }, { router, message }) {
      toLogout()
        .then(() => {
          commit("clearUser");
          dispatch("PermissionModule/clearPermissions", null, { root: true });
          dispatch("MenuStateModule/clearAllMenus", null, { root: true });
          dispatch("LockModule/clearLock", null, { root: true });
          router.push("/auth/login");
        })
        .catch((error) => {
          if (!error.__handled) {
            message?.error("退出登录失败，请稍后重试");
          }
        });
    }
  },
  getters: {
    id: state => state.userinfo.id,
    username: state => state.userinfo.username,
    avatar: state => state.userinfo.avatar,
    email: state => state.userinfo.email
  }
};
