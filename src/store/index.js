import { createStore } from 'vuex';

/* global toastr */

const store = createStore({
  state() {
    return {
      taskType: null,
      jsonData: null,
      calculatedSchemeData: null,
      linesData: [],
      polygonsData: [],
      coordsData: [],
      isUpdated: false,
      isLoading: false,

      stageData: {},

      // soils: [
      //   {
      //     name: 'Surface1',
      //     material: {
      //       'Грунт 1': {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 1,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      //   {
      //     name: 'Surface2',
      //     material: {
      //       'Мат 1': {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 10,
      //         tempHeat: 1,
      //         tempDensity: 2,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      // ],
      // lines: [
      //   {
      //     name: 'Line1',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 0,
      //       initialTemp: 0,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line3',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: -2,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line8',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: -2,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line10',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line11',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line12',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line13',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line14',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      // ],
      // timeSteps: {
      //   calcTime: '100',
      //   numSteps: '10',
      // },

      // Initial_phase: {
      //   soils: [
      //     {
      //       name: 'Surface1',
      //       material: {
      //         Material_1: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 50000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface2',
      //       material: {
      //         Material_2: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 10000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface3',
      //       material: {
      //         Material_3: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 30000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface4',
      //       material: {
      //         Material_3: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 30000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface5',
      //       material: {
      //         Material_2: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 10000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface6',
      //       material: {
      //         Material_3: {
      //           weight: 20,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 30000000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface7',
      //       material: {
      //         Material_3: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 30000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface8',
      //       material: {
      //         Material_2: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 10000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface9',
      //       material: {
      //         Material_2: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 10000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //     {
      //       name: 'Surface10',
      //       material: {
      //         Material_3: {
      //           weight: 0,
      //           poisson: 0.3,
      //           mechParameter: 'linear-elastic',
      //           elasticModulus: 30000,
      //         },
      //       },
      //       phaseActivity: true,
      //       comment: '',
      //     },
      //   ],
      //   lines: [
      //     {
      //       name: 'Line1',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0, uy: 0 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line2',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line3',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line4',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line7',
      //       phaseActivity: true,
      //       propertyParams: { q: 50 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line12',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line13',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0 },
      //       comment: '',
      //     },
      //     {
      //       name: 'Line14',
      //       phaseActivity: true,
      //       propertyParams: { ux: 0 },
      //       comment: '',
      //     },
      //   ],
      // },

      // soils: [
      //   {
      //     name: 'Surface1',
      //     material: {
      //       'Грунт 1': {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 1,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      //   {
      //     name: 'Surface2',
      //     material: {
      //       'Мат 1': {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 2,
      //         tempHeat: 2,
      //         tempDensity: 2,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      // ],
      // lines: [
      //   {
      //     name: 'Line1',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 0,
      //       initialTemp: 0,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line5',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: -2,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line7',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line8',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 5,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line9',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: -2,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      // ],
      // timeSteps: {
      //   calcTime: '100',
      //   numSteps: '100',
      // },

      // soils: [
      //   {
      //     name: 'Surface1',
      //     material: {
      //       'Грунт 1': {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 2,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      //   {
      //     name: 'Surface2',
      //     material: {
      //       Мат_2: {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 0.01,
      //         tempHeat: 100,
      //         tempDensity: 2,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      // ],
      // lines: [
      //   {
      //     name: 'Line1',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 0,
      //       initialTemp: 0,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line5',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: -2,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line7',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 10,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line8',
      //     phaseActivity: true,
      //     propertyParams: {
      //       boundaryTemp: 10,
      //       initialTemp: -2,
      //     },
      //     comment: '',
      //   },
      // ],
      // timeSteps: {
      //   calcTime: '100',
      //   numSteps: '100',
      // },

      // {
      //   Initial_phase: {
      //     soils: [
      //       {
      //         name: 'Surface1',
      //         material: {
      //           Material_1: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 50000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface2',
      //         material: {
      //           Material_2: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 10000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface3',
      //         material: {
      //           Material_3: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 30000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface4',
      //         material: {
      //           Material_3: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 30000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface5',
      //         material: {
      //           Material_2: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 10000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface6',
      //         material: {
      //           Material_3: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 30000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface7',
      //         material: {
      //           Material_3: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 30000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface8',
      //         material: {
      //           Material_2: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 10000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface9',
      //         material: {
      //           Material_2: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 10000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //       {
      //         name: 'Surface10',
      //         material: {
      //           Material_3: {
      //             weight: 0,
      //             poisson: 0.3,
      //             mechParameter: 'linear-elastic',
      //             elasticModulus: 30000,
      //           },
      //         },
      //         phaseActivity: true,
      //         comment: '',
      //       },
      //     ],
      //     lines: [
      //       {
      //         name: 'Line1',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //           uy: 0,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line2',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line3',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line4',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line7',
      //         phaseActivity: true,
      //         propertyParams: {
      //           q: 50,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line12',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line13',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //         },
      //         comment: '',
      //       },
      //       {
      //         name: 'Line14',
      //         phaseActivity: true,
      //         propertyParams: {
      //           ux: 0,
      //         },
      //         comment: '',
      //       },
      //     ],
      //   },
      // }

      // soils: [
      //   {
      //     name: 'Surface1',
      //     material: {
      //       Material_1: {
      //         weight: 20,
      //         poisson: 0.3,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 50000,
      //         filtrationX: 10,
      //         filtrationY: 20,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 1,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      //   {
      //     name: 'Surface2',
      //     material: {
      //       Material_2: {
      //         weight: 20,
      //         poisson: 0.3,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 10000,
      //         filtrationX: 1,
      //         filtrationY: 2,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 1,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      // ],
      // lines: [
      //   {
      //     name: 'Line2',
      //     phaseActivity: true,
      //     propertyParams: {
      //       ux: 0,
      //       uy: 0,
      //       nodalPressure: 5,
      //       boundaryTemp: 1,
      //       initialTemp: 10,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line6',
      //     phaseActivity: true,
      //     propertyParams: {
      //       ux: 0,
      //       uy: 0,
      //       nodalPressure: 10,
      //       boundaryTemp: 2,
      //       initialTemp: 5,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line7',
      //     phaseActivity: true,
      //     propertyParams: {
      //       ux: 0,
      //       uy: 0,
      //       nodalPressure: 10,
      //       boundaryTemp: 2,
      //       initialTemp: 2,
      //     },
      //     comment: '',
      //   },
      // ],
      // timeSteps: {
      //   calcTime: '500',
      //   numSteps: '10',
      // },

      // soils: [
      //   {
      //     name: 'Surface1',
      //     material: {
      //       Мат_1: {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         filtrationX: 1,
      //         filtrationY: 1,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      //   {
      //     name: 'Surface2',
      //     material: {
      //       Мат_2: {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         filtrationX: 1,
      //         filtrationY: 1,
      //       },
      //     },
      //     phaseActivity: true,
      //     comment: '',
      //   },
      // ],
      // lines: [
      //   {
      //     name: 'Line2',
      //     phaseActivity: true,
      //     propertyParams: {
      //       nodalPressure: 4,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line6',
      //     phaseActivity: true,
      //     propertyParams: {
      //       nodalPressure: 9,
      //     },
      //     comment: '',
      //   },
      //   {
      //     name: 'Line7',
      //     phaseActivity: true,
      //     propertyParams: {
      //       nodalPressure: 9,
      //     },
      //     comment: '',
      //   },
      // ],

      propertiesData: {},

      // linesProperties: [
      //   {
      //     Line1: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      //   {
      //     Line9: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      // ],
      // polygonsProperties: [
      //   {
      //     Surface1: 'material',
      //   },
      //   {
      //     Surface2: 'material',
      //   },
      //   {
      //     Surface3: 'material',
      //   },
      // ],

      // linesProperties: [
      //   {
      //     Line2: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      //   {
      //     Line6: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      //   {
      //     Line7: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      // ],
      // polygonsProperties: [
      //   {
      //     Surface1: 'material',
      //   },
      //   {
      //     Surface2: 'material',
      //   },
      // ],

      // linesProperties: [
      //   {
      //     Line2: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      //   {
      //     Line6: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      //   {
      //     Line7: {
      //       plateProperty: false,
      //       loadProperty: false,
      //       spacerProperty: false,
      //       boundaryCondition: true,
      //     },
      //   },
      // ],
      // polygonsProperties: [
      //   {
      //     Surface1: 'material',
      //   },
      //   {
      //     Surface2: 'material',
      //   },
      // ],

      characteristicsData: {},

      // oneDimData: [],
      //   twoDimData: [
      //     {
      //       Mat_1: {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 1,
      //         tempHeat: 2,
      //         tempDensity: 2,
      //       },
      //     },
      //     {
      //       Mat_2: {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 0.1,
      //         tempHeat: 0.1,
      //         tempDensity: 2.1,
      //       },
      //     },
      //     {
      //       Mat_3: {
      //         weight: 0,
      //         poisson: 0,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 0,
      //         tempCoef: 10,
      //         tempHeat: 5,
      //         tempDensity: 1,
      //       },
      //     },
      //   ],

      // oneDimData: [],
      //   twoDimData: [
      //     {
      //       Material_1: {
      //         weight: 20,
      //         poisson: 0.3,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 50000,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 1,
      //       },
      //     },
      //     {
      //       Material_2: {
      //         weight: 20,
      //         poisson: 0.3,
      //         mechParameter: 'linear-elastic',
      //         elasticModulus: 10000,
      //         tempCoef: 1,
      //         tempHeat: 1,
      //         tempDensity: 1,
      //       },
      //     },
      //   ],
      // oneDimData: [],
      // twoDimData: [
      //   {
      //     Мат_1: {
      //       weight: 0,
      //       poisson: 0,
      //       mechParameter: 'linear-elastic',
      //       elasticModulus: 0,
      //       filtrationX: 1,
      //       filtrationY: 1,
      //     },
      //   },
      //   {
      //     Мат_2: {
      //       weight: 0,
      //       poisson: 0,
      //       mechParameter: 'linear-elastic',
      //       elasticModulus: 0,
      //       filtrationX: 1,
      //       filtrationY: 1,
      //     },
      //   },
      // ],
    };
  },
  mutations: {
    setIsUpdated(state, payload) {
      state.isUpdated = payload.isUpdated;
    },
    setIsLoading(state, payload) {
      state.isLoading = payload.isLoading;
    },
    showToast(_, payload) {
      toastr.options.progressBar = true;
      toastr.options.positionClass = 'toast-bottom-right';
      switch (payload.type) {
        case 'ok':
          toastr.success(payload.msg);
          break;
        case 'error':
          toastr.error(payload.msg);
          break;
        case 'warning':
          toastr.warning(payload.msg);
          break;
        case 'info':
          toastr.info(payload.msg);
          break;
      }
    },
    setTaskType(state, payload) {
      state.taskType = payload.taskType;
    },
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
    setStageData(state, payload) {
      state.stageData = payload.stageData;
    },
    setPropertiesData(state, payload) {
      state.propertiesData = payload.propertiesData;
    },
    setCharacteristicsData(state, payload) {
      state.characteristicsData = payload.characteristicsData;
    },
  },
  actions: {
    sendIsLoading(context, payload) {
      context.commit('setIsLoading', {
        isLoading: payload.isLoading,
      });
    },
    sendIsUpdated(context, payload) {
      context.commit('setIsUpdated', {
        isUpdated: payload.isUpdated,
      });
    },
    sendToast(context, payload) {
      context.commit('showToast', payload.toastInfo);
    },
    sendTaskType(context, payload) {
      context.commit('setTaskType', { taskType: payload.taskType });
    },
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
    sendStageData(context, payload) {
      context.commit('setStageData', { stageData: payload.stageData });
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
    taskType(state) {
      return state.taskType;
    },
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
    stageData(state) {
      return state.stageData;
    },
    propertiesData(state) {
      return state.propertiesData;
    },
    characteristicsData(state) {
      return state.characteristicsData;
    },
    isUpdated(state) {
      return state.isUpdated;
    },
    isLoading(state) {
      return state.isLoading;
    },
  },
});

export default store;
