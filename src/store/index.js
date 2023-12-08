import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      jsonData: null,
      calculatedSchemeData: null,
      linesData: [],
      polygonsData: [],
    };
  },
  mutations: {
    setData(state, payload) {
      state.jsonData = payload.jsonData;
      state.calculatedSchemeData = payload.calculatedSchemeData;
    },
    setLinesData(state, payload) {
      state.linesData = payload.linesData;
    },
    setPolygonsData(state, payload) {
      state.polygonsData = payload.polygonsData;
    },
  },
  actions: {
    sendDataFromFile(context, payload) {
      context.commit('setData', {
        jsonData: payload.jsonData,
        calculatedSchemeData: payload.calculatedSchemeData,
      });
    },
    sendLinesData(context, payload) {
      context.commit('setLinesData', { linesData: payload.linesData });
    },
    sendPolygonsData(context, payload) {
      context.commit('setPolygonsData', { polygonsData: payload.polygonsData });
    },
  },
  getters: {
    gmshData(state) {
      return state.jsonData;
    },
    calculatedSchemeData(state) {
      return state.calculatedSchemeData;
    },
    linesData(state) {
      return state.linesData;
    },
    polygonsData(state) {
      return state.polygonsData;
    },
  },
});

export default store;
