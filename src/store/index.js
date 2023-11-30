import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      data: null,
    };
  },
  mutations: {
    setData(state, payload) {
      state.data = payload.data;
    },
  },
  actions: {
    getDataFromFile(context, payload) {
      context.commit('setData', { data: payload.data });
    },
  },
  getters: {
    dataGmsh(state) {
      return state.data;
    },
  },
});

export default store;
