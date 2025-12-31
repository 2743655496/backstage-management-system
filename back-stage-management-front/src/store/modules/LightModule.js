// store/modules/LightModule.js

// 抽一个纯函数，专门负责根据 isLight 设置所有主题字段
function applyTheme(state, isLight) {
  state.isLightOn = isLight
  state.backgroundColor = isLight ? "white" : "#000000"
  state.textColor = isLight ? "#000000" : "white"
  state.activeColor = isLight ? "#409EFF" : "#66b1ff"
  state.hoverColor = isLight ? "#ecf5ff" : "#242424"
  state.buttonHoverColor = isLight ? "#f5f5f5" : "#242424"
  state.el_breadcrumb_color = "#909399"
  state.el_breadcrumb_last_color = isLight ? "#303133" : "white"
  state.border_color = isLight ? "#ebeef5" : "#909399"

  // tab 配色
  state.tab_boder_color = isLight ? "#409eff" : "white"
  state.tab_background_color = isLight ? "#ecf5ff" : "#242424"

  // TabSwitcher
  state.tabSwitcherBgColor = isLight ? "#ecf0f1" : "#2a2a2a"
  state.tabSwitcherActiveBgColor = isLight ? "#ffffff" : "#3a3a3a"
  state.tabSwitcherTextColor = isLight ? "#7f8c8d" : "#b4b4b4"
  state.tabSwitcherActiveTextColor = isLight ? "#2c3e50" : "#ffffff"

  // 主页面背景
  state.mainBackgroundColor = isLight ? "#f5f7fa" : "#121212"
  state.subBackgroundColor = isLight ? "white" : "#1e1e1e"

  // 卡片文字
  state.cardTitleColor = isLight ? "#7f8c8d" : "#b4b4b4"
  state.cardValueColor = isLight ? "#2c3e50" : "#e0e0e0"
  state.cardSubtitleColor = isLight ? "#95a5a6" : "#8c8c8c"

  // 表格主题（亮/暗）
  state.tableBackgroundColor = isLight ? "#ffffff" : "black"
  state.tableTextColor = isLight ? "#303133" : "#d0d0d0"
  state.tableHeaderBackgroundColor = isLight ? "#f5f7fa" : "#2a2a2a"
  state.tableHeaderTextColor = isLight ? "#606266" : "#e0e0e0"

  // ⭐ 表格 hover 行颜色（亮/暗）——已按大众审美优化
  state.tableRowHoverBackgroundColor = isLight
    ? "#f0f7ff"   // 亮色 hover：柔和淡蓝
    : "#2a2a2a"   // 暗色 hover：深灰微亮
}

const state = {
  isLightOn: true, // 默认开灯（白天）
  backgroundColor: "white",
  textColor: "#000000",
  activeColor: "#409EFF",
  hoverColor: "#ecf5ff",
  buttonHoverColor: "#f5f5f5",
  el_breadcrumb_color:"#909399",
  el_breadcrumb_last_color:"#303133",
  border_color:"#ebeef5",

  // tab
  tab_boder_color:"#409eff",
  tab_background_color:"#ecf5ff",

  // 主页面背景 & 子页面背景 
  mainBackgroundColor: "#f5f7fa",
  subBackgroundColor: "white",

  /**
   * 分析页
   */
  cardTitleColor: "#7f8c8d",
  cardValueColor: "#2c3e50",
  cardSubtitleColor: "#95a5a6",

  // TabSwitcher
  tabSwitcherBgColor: "#ecf0f1",
  tabSwitcherActiveBgColor: "#ffffff",
  tabSwitcherTextColor: "#7f8c8d",
  tabSwitcherActiveTextColor: "#2c3e50",

  /**
   * 表格主题
   */
  tableBackgroundColor: "#ffffff",
  tableTextColor: "#303133",
  tableHeaderBackgroundColor: "#f5f7fa",
  tableHeaderTextColor: "#606266",

  // ⭐ 表格 hover 行背景色（默认亮色）
  tableRowHoverBackgroundColor: "#f0f7ff",
}

const getters = {
  isLightOn: (state) => state.isLightOn,
  backgroundColor: (state) => state.backgroundColor,
  textColor: (state) => state.textColor,
  activeColor: (state) => state.activeColor,
  hoverColor: (state) => state.hoverColor,
  buttonHoverColor: (state) => state.buttonHoverColor,
  el_breadcrumb_color: (state) => state.el_breadcrumb_color,
  el_breadcrumb_last_color: (state) => state.el_breadcrumb_last_color,
  border_color: (state) => state.border_color,

  tab_boder_color: (state) => state.tab_boder_color,
  tab_background_color: (state) => state.tab_background_color,

  // TabSwitcher
  tabSwitcherBgColor: (state) => state.tabSwitcherBgColor,
  tabSwitcherActiveBgColor: (state) => state.tabSwitcherActiveBgColor,
  tabSwitcherTextColor: (state) => state.tabSwitcherTextColor,
  tabSwitcherActiveTextColor: (state) => state.tabSwitcherActiveTextColor,

  mainBackgroundColor: (state) => state.mainBackgroundColor,
  subBackgroundColor: (state) => state.subBackgroundColor,

  cardTitleColor: (state) => state.cardTitleColor,
  cardValueColor: (state) => state.cardValueColor,
  cardSubtitleColor: (state) => state.cardSubtitleColor,

  // 表格主题
  tableBackgroundColor: (state) => state.tableBackgroundColor,
  tableTextColor: (state) => state.tableTextColor,
  tableHeaderBackgroundColor: (state) => state.tableHeaderBackgroundColor,
  tableHeaderTextColor: (state) => state.tableHeaderTextColor,
  tableRowHoverBackgroundColor: (state) => state.tableRowHoverBackgroundColor,
}

const mutations = {
  SET_LIGHT_STATE(state, payload) {
    applyTheme(state, payload)
  },

  TOGGLE_LIGHT(state) {
    const next = !state.isLightOn
    applyTheme(state, next)
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
