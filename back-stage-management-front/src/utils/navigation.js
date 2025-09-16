// src/utils/navigation.js

export default {
  /**
   * 判断是否需要跳转
   * @param {Object} vueInstance - 当前组件实例（通常是 this）
   * @param {String} path - 目标路径
   * @returns {Boolean}
   */
  shouldNavigate(vueInstance, path) {
    return path && vueInstance.$route.path !== path
  },

  /**
   * 安全跳转（避免重复导航）
   * @param {Object} vueInstance - 当前组件实例（通常是 this）
   * @param {String} path - 目标路径
   */
  safePush(vueInstance, path) {
    if (this.shouldNavigate(vueInstance, path)) {
      vueInstance.$router.push(path)
    }
  }
}


