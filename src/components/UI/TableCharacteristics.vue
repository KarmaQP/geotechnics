<template>
  <div class="characteristics-container">
    <div class="table">
      <div class="tr tr--header">
        <div class="th">Наименование объекта</div>
        <div class="th">Общие параметры</div>
        <div class="th">Значение</div>
      </div>
      <div class="generated-table">
        <div class="toggle-container">
          <div @click="togglePolygons">
            {{ polygonsLabel }} полигоны (размер: {{ polygonsData.length }})
          </div>
          <i
            class="fa-solid"
            :class="polygonsArrowState"
            @click="togglePolygons"
          ></i>
        </div>
      </div>
      <two-dimensions
        v-for="polygonData in polygonsData"
        v-show="showPolygons"
        :key="polygonData[0]"
        :id="polygonData[0]"
        :material-name="polygonData[0]"
      ></two-dimensions>
      <div class="generated-table">
        <div class="toggle-container">
          <div @click="toggleLines">
            {{ linesLabel }} линии (размер: {{ linesData.length }})
          </div>
          <i class="fa-solid" :class="linesArrowState" @click="toggleLines"></i>
        </div>
      </div>
      <one-dimension-element
        v-for="lineData in linesData"
        v-show="showLines"
        :key="lineData[0]"
        :id="lineData[0]"
        :material-name="lineData[0]"
      ></one-dimension-element>
    </div>
    <button type="button" @click="applyCharacteristics">
      Применить характеристики
    </button>
  </div>
</template>

<script>
import TwoDimensions from './Table/TableCharacteristics/TwoDimensions.vue';
import OneDimensionElement from './Table/TableCharacteristics/OneDimensionElement.vue';
// import OneDimensionPoint from './Table/TableCharacteristics/OneDimensionPoint.vue';

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';

export default {
  components: {
    TwoDimensions,
    OneDimensionElement,
    // OneDimensionPoint,
  },
  props: ['linesData', 'polygonsData'],
  data() {
    return {
      showPolygons: false,
      showLines: false,
    };
  },
  computed: {
    ...mapGetters(['characteristicsData']),
    linesArrowState() {
      if (this.showLines) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
    polygonsArrowState() {
      if (this.showPolygons) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
    linesLabel() {
      if (this.showLines) return 'Скрыть';
      else return 'Показать';
    },
    polygonsLabel() {
      if (this.showPolygons) return 'Скрыть';
      else return 'Показать';
    },
  },
  methods: {
    ...mapActions(['sendCharacteristicsData']),
    toggleLines() {
      this.showLines = !this.showLines;
    },
    togglePolygons() {
      this.showPolygons = !this.showPolygons;
    },
    applyCharacteristics() {
      let pData = [];
      let lData = [];

      // NOTE: filling polygons data from selected inputs
      this.polygonsData.forEach((polygonData, i) => {
        const polygonId = polygonData[0].toLowerCase();
        const mechParameter = document.querySelector(
          `#mech-parameter-${polygonId}`
        );
        const weightValue = Number(
          document.querySelector(`#weight-${polygonId}`).value
        );
        const poissonValue = Number(
          document.querySelector(`#poisson-${polygonId}`).value
        );

        console.log(mechParameter.value);
        if (mechParameter.value === 'linear-elastic') {
          const linearElasticValue = Number(
            document.querySelector(`#linear-elastic-${polygonId}`).value
          );

          pData.push({
            [polygonData[0]]: {
              weight: weightValue,
              poisson: poissonValue,
              mechParameter: mechParameter.value,
              elasticModulus: linearElasticValue,
            },
          });
        } else if (mechParameter.value === 'mohr-coloumb') {
          const mohrColoumbData = document.querySelectorAll(
            `#mohr-coloumb-${polygonId}`
          );

          pData.push({
            [polygonData[0]]: {
              weight: weightValue,
              poisson: poissonValue,
              mechParameter: mechParameter.value,
            },
          });

          mohrColoumbData.forEach((input, j) => {
            switch (j) {
              // elastic modulus
              case 0:
                pData[i][polygonData[0]].elasticModulus = Number(input.value);
                break;
              // internal friction angle
              case 1:
                pData[i][polygonData[0]].internalFrictionAngle = Number(
                  input.value
                );
                break;
              // adhesion
              case 2:
                pData[i][polygonData[0]].adhesion = Number(input.value);
                break;
              // dilatancy angle
              case 3:
                pData[i][polygonData[0]].dilatancyAngle = Number(input.value);
                break;
              // tensile strength
              case 4:
                pData[i][polygonData[0]].tensileStrength = Number(input.value);
                break;
            }
          });
        } else if (mechParameter.value === 'cam-clay') {
          const camClayData = document.querySelectorAll(
            `#cam-clay-${polygonId}`
          );

          pData.push({
            [polygonData[0]]: {
              weight: weightValue,
              poisson: poissonValue,
              mechParameter: mechParameter.value,
            },
          });

          camClayData.forEach((input, j) => {
            switch (j) {
              // compression index
              case 0:
                pData[i][polygonData[0]].compressionIndex = Number(input.value);
                break;
              // recompression index
              case 1:
                pData[i][polygonData[0]].recompressionIndex = Number(
                  input.value
                );
                break;
              // mcsl
              case 2:
                pData[i][polygonData[0]].mscl = Number(input.value);
                break;
            }
          });
        } else {
          // throw error
          console.error('Error: unexpected select value.');
          return;
        }
      });

      // NOTE: filling lines data from inputs/select
      const inputsElasticModulus =
        document.querySelectorAll('#elastic-modulus');
      const inputsSectionalArea = document.querySelectorAll('#sectional-area');
      const inputsInertiaMoment = document.querySelectorAll('#inertia-moment');
      const selectsWorkType = document.querySelectorAll('#work-type');

      this.linesData.forEach((lineData, i) => {
        const weightValue = Number(
          document.querySelector(`#line-weight-${lineData[0]}`).value
        );
        const poissonValue = Number(
          document.querySelector(`#line-poisson-${lineData[0]}`).value
        );

        lData.push({
          [lineData[0]]: {
            weight: weightValue,
            poisson: poissonValue,
            elasticModulus: Number(inputsElasticModulus[i].value),
            sectionalArea: Number(inputsSectionalArea[i].value),
            inertiaMoment: Number(inputsInertiaMoment[i].value),
            workType: selectsWorkType[i].value,
          },
        });
      });

      this.sendCharacteristicsData({
        characteristicsData: {
          linesCharacteristics: lData,
          polygonsCharacteristics: pData,
        },
      });

      console.log(this.characteristicsData);
    },
  },
};
</script>

<style scoped>
.tr {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

i {
  cursor: pointer;
  min-width: 1%;
}

.toggle-container {
  font-weight: bold;
  padding: 0.8rem 0.4rem;
  display: flex;
  justify-content: space-between;
}

.toggle-container div {
  min-width: 98%;
  cursor: pointer;
}

.characteristics-container {
  text-align: right;
}

.table {
  text-align: left;
}

button {
  margin-top: 2.4rem;
  padding: 0.8rem;
  background-color: var(--blue-bg-color);
  color: var(--text-color);
  font-size: 1.4rem;
  transition: all 0.3s;
}

button:hover {
  background-color: var(--hover-blue-bg-color);
}

button:active {
  background-color: var(--active-blue-bg-color);
}
</style>
