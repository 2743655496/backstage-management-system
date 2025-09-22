import { v4 as uuidv4 } from 'uuid';

const state = {
  chartRenderKey: uuidv4()
};

const mutations = {
  UPDATE_CHART_KEY(state) {
    state.chartRenderKey = uuidv4(); // 每次生成新 key
  }
};

const actions = {
  triggerChartRemount({ commit }) {
    commit('UPDATE_CHART_KEY');
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
