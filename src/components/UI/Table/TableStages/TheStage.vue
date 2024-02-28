<template>
  <button class="bubble btn">{{ stageName }}</button>
  <soil-table></soil-table>
  <line-table></line-table>
  <div class="table" v-if="taskType === 'temperature'">
    <div class="tr two-cols">
      <div class="th">Параметр</div>
      <div class="th">Величина</div>
    </div>
    <div class="generated-table">
      <div class="tr two-cols">
        <div class="td">Время расчета, с</div>
        <div class="td">
          <input
            type="number"
            id="input__calc-time"
            placeholder="Введите время..."
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr two-cols">
        <div class="td">Кол-во шагов интегрирования по времени</div>
        <div class="td">
          <input
            type="number"
            id="input__num-steps"
            placeholder="Введите количество шагов..."
          />
        </div>
      </div>
    </div>
  </div>
  <div class="btn__container">
    <button type="button" @click="applyStage">Применить</button>
  </div>

  <!-- <point-table></point-table> -->
</template>

<script>
import SoilTable from './SoilTable.vue';
import LineTable from './LineTable.vue';
// import PointTable from './PointTable.vue';
import { mapActions } from 'vuex';
import { mapGetters } from 'vuex';

export default {
  components: {
    SoilTable,
    LineTable,
    // PointTable,
  },
  data() {
    return {
      twoDimData: null,
      oneDimData: null,
      rawStageData: {
        soils: [],
        lines: [],
      },
    };
  },
  props: ['stageName'],
  computed: {
    ...mapGetters([
      'taskType',
      'characteristicsData',
      'propertiesData',
      'linesData',
      'polygonsData',
      'stageData',
    ]),
  },
  methods: {
    ...mapActions(['sendStageData', 'sendToast', 'sendIsUpdated']),
    applyStage() {
      // NOTE: filling stage data: soils
      this.propertiesData.polygonsProperties.forEach((propertyData) => {
        const [soilName] = [...Object.keys(propertyData)];

        const selectMaterialValue = document.querySelector(
          `#select__material--${soilName.toLowerCase()}`
        ).value;

        const selectedMaterial = Object.values(
          this.characteristicsData.twoDimData
        ).find((charData) => Object.keys(charData)[0] === selectMaterialValue);

        const selectedActivityValue =
          document.querySelector(`#select__activity--${soilName.toLowerCase()}`)
            .value === 'true';

        const comment = document.querySelector(
          `#input__comment--${soilName.toLowerCase()}`
        ).value;

        this.rawStageData.soils.push({
          name: soilName,
          material: selectedMaterial ? selectedMaterial : null,
          phaseActivity: selectedActivityValue,
          comment: comment,
        });
      });

      // NOTE: filling stage data: lines
      this.propertiesData.linesProperties.forEach((propertyData) => {
        const [lineName] = [...Object.keys(propertyData)];

        const selectedActivityValue =
          document.querySelector(`#select__activity--${lineName.toLowerCase()}`)
            .value === 'true';

        let propertyParams = {};

        console.log(this.taskType);

        // boundaryCondition
        if (Object.values(propertyData)[0].boundaryCondition) {
          if (this.taskType === 'elasticity-nonlinearity') {
            const uxValue = document.querySelector(
              `#input__bound-x--${lineName.toLowerCase()}`
            ).value;
            const uyValue = document.querySelector(
              `#input__bound-y--${lineName.toLowerCase()}`
            ).value;

            if (uxValue !== '') propertyParams.ux = Number(uxValue);
            if (uyValue !== '') propertyParams.uy = Number(uyValue);
          } else if (this.taskType === 'filtration') {
            const nodalPressureValue = document.querySelector(
              `#input__nodal-pressure--${lineName.toLowerCase()}`
            ).value;

            propertyParams.nodalPressure = Number(nodalPressureValue);
          } else if (this.taskType === 'temperature') {
            const tempValue = document.querySelector(
              `#input__temperature--${lineName.toLowerCase()}`
            ).value;
            const initialTempValue = document.querySelector(
              `#input__initial-temperature--${lineName.toLowerCase()}`
            ).value;

            propertyParams.boundaryTemp = Number(tempValue);
            propertyParams.initialTemp = Number(initialTempValue);
          }
        }

        // loadProperty
        if (Object.values(propertyData)[0].loadProperty) {
          const qValue = Number(
            document.querySelector(`#input__load--${lineName.toLowerCase()}`)
              .value
          );

          propertyParams.q = qValue;
        }

        // platerProperty
        if (Object.values(propertyData)[0].plateProperty) {
          const selectedPlateValue = document.querySelector(
            `#select__plate--${lineName.toLowerCase()}`
          ).value;
          const selectedMaterial = Object.values(
            this.characteristicsData.oneDimData
          ).find((charData) => Object.keys(charData)[0] === selectedPlateValue);

          propertyParams.plateMaterial = selectedMaterial
            ? selectedMaterial
            : null;
        }

        // spacerProperty
        if (Object.values(propertyData)[0].spacerProperty) {
          const selectedSpacerValue = document.querySelector(
            `#select__spacer--${lineName.toLowerCase()}`
          ).value;
          const selectedMaterial = Object.values(
            this.characteristicsData.oneDimData
          ).find(
            (charData) => Object.keys(charData)[0] === selectedSpacerValue
          );

          propertyParams.spacerMaterial = selectedMaterial
            ? selectedMaterial
            : null;
        }

        const comment = document.querySelector(
          `#input__comment--${lineName.toLowerCase()}`
        ).value;

        this.rawStageData.lines.push({
          name: lineName,
          phaseActivity: selectedActivityValue,
          propertyParams: propertyParams,
          comment: comment,
        });
      });

      if (this.taskType === 'temperature') {
        const calcTimeValue = document.querySelector('#input__calc-time').value;
        const numStepsValue = document.querySelector('#input__num-steps').value;

        this.rawStageData.timeSteps = {
          calcTime: calcTimeValue,
          numSteps: numStepsValue,
        };
      }

      let initialStageData = { Initial_phase: {} };
      if (this.taskType === 'elasticity-nonlinearity') {
        initialStageData.Initial_phase = this.rawStageData;
        this.sendStageData({ stageData: {} });
        this.sendStageData({ stageData: initialStageData });
      } else {
        // console.log(this.rawStageData);
        this.sendStageData({ stageData: {} });
        this.sendStageData({ stageData: this.rawStageData });
      }

      this.rawStageData = {
        soils: [],
        lines: [],
      };

      console.log(this.stageData);
      this.sendToast({
        toastInfo: {
          msg: 'Данные расчетного этапа успешно сохранены!',
          type: 'ok',
        },
      });

      this.sendIsUpdated({ isUpdated: true });
    },
  },
  // beforeMount() {
  //   this.twoDimData = this.characteristicsData.twoDimData;
  //   this.oneDimData = this.characteristicsData.oneDimData;
  // },
  // updated() {
  //   this.twoDimData = this.characteristicsData.twoDimData;
  //   this.oneDimData = this.characteristicsData.oneDimData;

  //   console.log('Updated TheStage');
  // },
};
</script>

<style scoped>
.table {
  text-align: left;
}

.table {
  margin-top: 3.2rem;
}

.two-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* .btn {
  font-size: 2rem;
  margin-top: 3.2rem;
}
.btn:first-child {
  margin-top: 0;
} */

.btn__container {
  text-align: right;
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
