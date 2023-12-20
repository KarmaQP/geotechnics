import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      jsonData: null,
      calculatedSchemeData: null,
      linesData: [],
      polygonsData: [],
      propertiesData: [],
      characteristicsData: {
        oneDimData: [
          {
            'Хар_1 (1d)': {
              weight: 1,
              poisson: 2,
              elasticModulus: 3,
              sectionalArea: 4,
              inertiaMoment: 5,
              workType: 'stretching-compression',
            },
          },
          {
            'Хар_2 (1d)': {
              weight: 6,
              poisson: 7,
              elasticModulus: 8,
              sectionalArea: 9,
              inertiaMoment: 10,
              workType: 'stretching-compression-bending',
            },
          },
          {
            'Хар_3 (1d)': {
              weight: 11,
              poisson: 12,
              elasticModulus: 13,
              sectionalArea: 14,
              inertiaMoment: 15,
              workType: 'stretching-compression-bending',
            },
          },
        ],
        twoDimData: [
          {
            'Хар_1 (2d)': {
              weight: 1,
              poisson: 2,
              mechParameter: 'linear-elastic',
              elasticModulus: 3,
            },
          },
          {
            'Хар_2 (2d)': {
              weight: 4,
              poisson: 5,
              mechParameter: 'mohr-coloumb',
              elasticModulus: 6,
              internalFrictionAngle: 7,
              adhesion: 8,
              dilatancyAngle: 9,
              tensileStrength: 10,
            },
          },
          {
            'Хар_3 (2d)': {
              weight: 11,
              poisson: 12,
              mechParameter: 'cam-clay',
              compressionIndex: 13,
              recompressionIndex: 14,
              mscl: 15,
            },
          },
        ],
      },
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
