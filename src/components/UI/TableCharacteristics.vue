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
          <div @click="toggleTwoDim">
            {{ twoDimLabel }} 2d характеристики (размер: {{ countTwoDimRows }})
          </div>
          <i
            class="fa-solid"
            :class="twoDimArrowState"
            @click="toggleTwoDim"
          ></i>
        </div>
      </div>
      <two-dimensions
        v-for="i in countTwoDimRows"
        v-show="showTwoDim"
        :key="i"
        :id="i"
      ></two-dimensions>
      <div class="btn-add__container" v-show="showTwoDim">
        <button class="add-dim" @click="addTwoDim">
          Добавить характеристику
        </button>
      </div>
      <div class="generated-table">
        <div class="toggle-container">
          <div @click="toggleOneDim">
            {{ oneDimLabel }} 1d характеристики (размер: {{ countOneDimRows }})
          </div>
          <i
            class="fa-solid"
            :class="oneDimArrowState"
            @click="toggleOneDim"
          ></i>
        </div>
      </div>
      <one-dimension-element
        v-for="i in countOneDimRows"
        v-show="showOneDim"
        :key="i"
        :id="i"
      ></one-dimension-element>
      <div class="btn-add__container" v-show="showOneDim">
        <button class="add-dim" @click="addOneDim">
          Добавить характеристику
        </button>
      </div>
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
import axios from 'axios';

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';

export default {
  components: {
    TwoDimensions,
    OneDimensionElement,
    // OneDimensionPoint,
  },
  data() {
    return {
      showTwoDim: false,
      showOneDim: false,
      countTwoDimRows: 0,
      twoDimData: [],
      selectedTwoDimId: null,
      countOneDimRows: 0,
      oneDimData: [],
      selectedOneDimId: null,
    };
  },
  computed: {
    ...mapGetters(['characteristicsData']),
    oneDimArrowState() {
      if (this.showOneDim) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
    twoDimArrowState() {
      if (this.showTwoDim) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
    oneDimLabel() {
      if (this.showOneDim) return 'Скрыть';
      else return 'Показать';
    },
    twoDimLabel() {
      if (this.showTwoDim) return 'Скрыть';
      else return 'Показать';
    },
  },
  methods: {
    ...mapActions(['sendCharacteristicsData']),
    toggleOneDim() {
      this.showOneDim = !this.showOneDim;
    },
    toggleTwoDim() {
      this.showTwoDim = !this.showTwoDim;
    },
    addTwoDim() {
      this.countTwoDimRows++;
    },
    addOneDim() {
      this.countOneDimRows++;
    },
    async applyCharacteristics() {
      let twoDimData = [];
      let oneDimData = [];

      // NOTE: filling polygons data from selected inputs
      for (let i = 0; i < this.countTwoDimRows; i++) {
        const twoDimId = i + 1;
        const mechParameter = document.querySelector(
          `#mech-parameter-${twoDimId}`
        );
        const charName = document.querySelector(`#name-${twoDimId}`).value;
        const weightValue = Number(
          document.querySelector(`#weight-${twoDimId}`).value
        );
        const poissonValue = Number(
          document.querySelector(`#poisson-${twoDimId}`).value
        );

        console.log(mechParameter.value);
        if (mechParameter.value === 'linear-elastic') {
          const linearElasticValue = Number(
            document.querySelector(`#linear-elastic-${twoDimId}`).value
          );

          twoDimData.push({
            [charName]: {
              weight: weightValue,
              poisson: poissonValue,
              mechParameter: mechParameter.value,
              elasticModulus: linearElasticValue,
            },
          });
        } else if (mechParameter.value === 'mohr-coloumb') {
          const mohrColoumbData = document.querySelectorAll(
            `#mohr-coloumb-${twoDimId}`
          );

          twoDimData.push({
            [charName]: {
              weight: weightValue,
              poisson: poissonValue,
              mechParameter: mechParameter.value,
            },
          });

          mohrColoumbData.forEach((input, j) => {
            switch (j) {
              // elastic modulus
              case 0:
                twoDimData[i][charName].elasticModulus = Number(input.value);
                break;
              // internal friction angle
              case 1:
                twoDimData[i][charName].internalFrictionAngle = Number(
                  input.value
                );
                break;
              // adhesion
              case 2:
                twoDimData[i][charName].adhesion = Number(input.value);
                break;
              // dilatancy angle
              case 3:
                twoDimData[i][charName].dilatancyAngle = Number(input.value);
                break;
              // tensile strength
              case 4:
                twoDimData[i][charName].tensileStrength = Number(input.value);
                break;
            }
          });
        } else if (mechParameter.value === 'cam-clay') {
          const camClayData = document.querySelectorAll(
            `#cam-clay-${twoDimId}`
          );

          twoDimData.push({
            [charName]: {
              weight: weightValue,
              poisson: poissonValue,
              mechParameter: mechParameter.value,
            },
          });

          camClayData.forEach((input, j) => {
            switch (j) {
              // compression index
              case 0:
                twoDimData[i][charName].compressionIndex = Number(input.value);
                break;
              // recompression index
              case 1:
                twoDimData[i][charName].recompressionIndex = Number(
                  input.value
                );
                break;
              // mcsl
              case 2:
                twoDimData[i][charName].mscl = Number(input.value);
                break;
            }
          });
        } else {
          // throw error
          console.error('Error: unexpected select value.');
          return;
        }
      }

      // NOTE: filling lines data from inputs/select
      for (let i = 0; i < this.countOneDimRows; i++) {
        const oneDimId = i + 1;
        const weightValue = Number(
          document.querySelector(`#one-dim__weight-${oneDimId}`).value
        );
        const poissonValue = Number(
          document.querySelector(`#one-dim__poisson-${oneDimId}`).value
        );
        const charName = document.querySelector(
          `#one-dim__name-${oneDimId}`
        ).value;
        const inputsElasticModulus = document.querySelector(
          `#elastic-modulus-${oneDimId}`
        );
        const inputsSectionalArea = document.querySelector(
          `#sectional-area-${oneDimId}`
        );
        const inputsInertiaMoment = document.querySelector(
          `#inertia-moment-${oneDimId}`
        );
        const selectsWorkType = document.querySelector(
          `#work-type-${oneDimId}`
        );

        oneDimData.push({
          [charName]: {
            weight: weightValue,
            poisson: poissonValue,
            elasticModulus: Number(inputsElasticModulus.value),
            sectionalArea: Number(inputsSectionalArea.value),
            inertiaMoment: Number(inputsInertiaMoment.value),
            workType: selectsWorkType.value,
          },
        });
      }

      this.sendCharacteristicsData({
        characteristicsData: {
          oneDimData: oneDimData,
          twoDimData: twoDimData,
        },
      });

      console.log(this.characteristicsData);

      /* global $ */
      const formData = new FormData();
      const csrf = $('input[name=csrfmiddlewaretoken]').val();

      formData.append(
        'propertiesData',
        JSON.stringify(this.characteristicsData)
      );
      formData.append('csrfmiddlewaretoken', csrf);

      const response = await axios.post('api/test/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response);
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

.btn-add__container {
  background-color: var(--bg-color);
  padding: 1.2rem 0 1.8rem 0;
  display: flex;
  justify-content: center;
}

.add-dim {
  margin-top: 0 !important;
  transition: all 0.3s ease;
  font-size: 1.2rem;
}
</style>
