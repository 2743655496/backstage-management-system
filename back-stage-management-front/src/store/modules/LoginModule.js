export default {
  namespaced: true,
  //状态，数据
  state: {
    userinfo: JSON.parse(localStorage.getItem("userinfo")) || {
      id: '',
      username: '',
      avatar: '',
      email: '',
    }
  },
  //修改state里数据的唯一方式
  mutations: {
    /**
     * 设置用户信息
     */
    setUserInfo(state, payload) {
      state.userinfo = { ...payload };
      localStorage.setItem("userinfo", JSON.stringify(state.userinfo));
    },
    /**
     * 清空用户信息
     */
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
  },
  //包装数据，不修改
  getters: {
    id: state => state.userinfo.id,
    username: state => state.userinfo.username,
    avatar: state => state.userinfo.avatar,
    email: state => state.userinfo.email
  }
};