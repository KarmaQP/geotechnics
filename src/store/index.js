import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      jsonData: null,
      calculatedSchemeData: null,
      linesData: [],
      polygonsData: [],
      coordsData: [],
      propertiesData: {
        linesProperties: [
          {
            Line1: {
              plateProperty: true,
              loadProperty: false,
              spacerProperty: false,
              boundaryCondition: true,
            },
          },
          {
            Line2: {
              plateProperty: false,
              loadProperty: true,
              spacerProperty: true,
              boundaryCondition: false,
            },
          },
          {
            Line3: {
              plateProperty: true,
              loadProperty: true,
              spacerProperty: false,
              boundaryCondition: true,
            },
          },
          {
            Line29: {
              plateProperty: false,
              loadProperty: true,
              spacerProperty: true,
              boundaryCondition: true,
            },
          },
        ],
        polygonsProperties: [
          {
            Surface1: 'material',
          },
          {
            Surface2: 'material',
          },
          {
            Surface3: 'material',
          },
          {
            Surface4: 'material',
          },
          {
            Surface5: 'material',
          },
          {
            Surface6: 'material',
          },
          {
            Surface7: 'material',
          },
          {
            Surface8: 'material',
          },
          {
            Surface9: 'material',
          },
          {
            Surface10: 'material',
          },
        ],
      },
      characteristicsData: {
        oneDimData: [
          {
            'Хар_1 (1д)': {
              weight: 5,
              poisson: 4,
              elasticModulus: 3,
              sectionalArea: 6,
              inertiaMoment: 7,
              workType: 'stretching-compression',
            },
          },
          {
            'Хар_2 (1д)': {
              weight: 12,
              poisson: 3124,
              elasticModulus: 154,
              sectionalArea: 3145,
              inertiaMoment: 345,
              workType: 'stretching-compression-bending',
            },
          },
        ],
        twoDimData: [
          {
            Хар_1: {
              weight: 5,
              poisson: 3,
              mechParameter: 'linear-elastic',
              elasticModulus: 2,
            },
          },
          {
            Хар_2: {
              weight: 6,
              poisson: 4,
              mechParameter: 'linear-elastic',
              elasticModulus: 3,
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
    setCoordsData(state, payload) {
      state.coordsData = payload.coordsData;
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
    sendCoordsData(context, payload) {
      context.commit('setCoordsData', { coordsData: payload.coordsData });
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
    coordsData(state) {
      return state.coordsData;
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
