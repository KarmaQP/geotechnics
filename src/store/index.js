import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      jsonData: null,
      calculatedSchemeData: null,
      linesData: [],
      polygonsData: [],
      propertiesData: [],
      characteristicsData: [],
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
    setPropertiesData(state, payload) {
      state.propertiesData = payload.propertiesData;
    },
    setCharacteristicsData(state, payload) {
      state.characteristicsData = payload.characteristicsData;
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
    sendPropertiesData(context, payload) {
      context.commit('setPropertiesData', {
        propertiesData: payload.propertiesData,
      });
    },
    sendCharacteristicsData(context, payload) {
      context.commit('setCharacteristicsData', {
        characteristicsData: payload.characteristicsData,
      });
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
    propertiesData(state) {
      return state.propertiesData;
    },
    characteristicsData(state) {
      return state.characteristicsData;
    },
  },
});

export default store;
