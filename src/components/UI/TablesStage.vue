<template>
  <the-stage
    stage-name="Фаза инициализации"
    :task-type="taskType"
    stage-type="init"
  ></the-stage>
  <the-stage
    v-for="n in phasesNum"
    :key="n"
    :stage-name="`Фаза ${n}`"
    :task-type="taskType"
    stage-type="phase"
  ></the-stage>
  <temperature-table></temperature-table>
  <div class="btn__container">
    <button
      v-if="taskType === 'nonlinearity'"
      type="button"
      class="add__phase"
      @click="addPhase"
    >
      Добавить фазу
    </button>
    <button type="button" class="apply_stage" @click="applyStage">
      Применить
    </button>
  </div>
</template>

<script>
import TheStage from './Table/TableStages/TheStage.vue';
import TemperatureTable from './Table/TableStages/TemperatureTable.vue';
import { mapActions } from 'vuex';
import { mapGetters } from 'vuex';

export default {
  components: {
    TheStage,
    TemperatureTable,
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
      phasesNum: 0,
    };
  },
  computed: {
    ...mapGetters([
      'taskType',
      'characteristicsData',
      'propertiesData',
      // 'linesData',
      // 'polygonsData',
      'stageData',
    ]),
  },
  methods: {
    ...mapActions(['sendStageData', 'sendToast', 'sendIsUpdated']),
    addPhase() {
      this.phasesNum++;
    },
    applyStage() {
      // NOTE: filling stage data: soils
      let soilsData = [];
      let linesData = [];

      this.propertiesData.polygonsProperties.forEach((propertyData) => {
        const [soilName] = [...Object.keys(propertyData)];

        if (this.taskType === 'nonlinearity') {
          let selectedMaterialsArr = [];
          let selectedActivitiesArr = [];
          let commentsArr = [];

          const selectedMaterials = document.querySelectorAll(
            `#select__material--${soilName.toLowerCase()}`
          );

          selectedMaterials.forEach((input) =>
            selectedMaterialsArr.push(input.value)
          );

          const selectedActivityValues = document.querySelectorAll(
            `#select__activity--${soilName.toLowerCase()}`
          );
          selectedActivityValues.forEach((activityValue) =>
            selectedActivitiesArr.push(activityValue.value === 'true')
          );

          const comments = document.querySelectorAll(
            `#input__comment--${soilName.toLowerCase()}`
          );
          comments.forEach((comment) => commentsArr.push(comment.value));

          selectedMaterialsArr.forEach((material, i) => {
            if (!soilsData[i]) soilsData.push({ soils: [] });

            soilsData[i].soils.push({
              name: soilName,
              material: material,
              phaseActivity: selectedActivitiesArr[i],
              comment: commentsArr[i],
            });
          });
        } else {
          const selectedMaterialValue = document.querySelector(
            `#select__material--${soilName.toLowerCase()}`
          ).value;

          const selectedMaterial = Object.values(
            this.characteristicsData.twoDimData
          ).find(
            (charData) => Object.keys(charData)[0] === selectedMaterialValue
          );

          const selectedActivityValue =
            document.querySelector(
              `#select__activity--${soilName.toLowerCase()}`
            ).value === 'true';

          const comment = document.querySelector(
            `#input__comment--${soilName.toLowerCase()}`
          ).value;

          this.rawStageData.soils.push({
            name: soilName,
            material: selectedMaterial ? selectedMaterial : null,
            phaseActivity: selectedActivityValue,
            comment: comment,
          });
        }
      });

      // NOTE: filling stage data: lines
      this.propertiesData.linesProperties.forEach((propertyData) => {
        const [lineName] = [...Object.keys(propertyData)];

        if (this.taskType === 'nonlinearity') {
          let propertyParamsArr = [];
          let selectedPlatesArr = [];
          let selectedSpacersArr = [];
          let selectedActivitiesArr = [];
          let commentsArr = [];

          // activities array
          const selectedActivities = document.querySelectorAll(
            `#select__activity--${lineName.toLowerCase()}`
          );
          selectedActivities.forEach((activity) =>
            selectedActivitiesArr.push(activity.value === 'true')
          );

          // comments array
          const comments = document.querySelectorAll(
            `#input__comment--${lineName.toLowerCase()}`
          );
          comments.forEach((comment) => {
            commentsArr.push(comment.value);
          });

          // boundary conditions
          if (Object.values(propertyData)[0].boundaryCondition) {
            const uxInputs = document.querySelectorAll(
              `#input__bound-x--${lineName.toLowerCase()}`
            );
            const uyInputs = document.querySelectorAll(
              `#input__bound-y--${lineName.toLowerCase()}`
            );

            uxInputs.forEach((_, i) => {
              if (!propertyParamsArr[i]) propertyParamsArr.push({});

              if (uxInputs[i].value !== '')
                propertyParamsArr[i].ux = Number(uxInputs[i].value);
              if (uyInputs[i].value !== '')
                propertyParamsArr[i].uy = Number(uyInputs[i].value);
            });
          }

          // loadProperty
          if (Object.values(propertyData)[0].loadProperty) {
            const qInputs = document.querySelectorAll(
              `#input__load--${lineName.toLowerCase()}`
            );

            qInputs.forEach((input, i) => {
              if (!propertyParamsArr[i]) propertyParamsArr.push({});

              propertyParamsArr[i].q = Number(input.value);
            });
          }

          // platerProperty
          if (Object.values(propertyData)[0].plateProperty) {
            const selectedPlates = document.querySelectorAll(
              `#select__material--${lineName.toLowerCase()}`
            );

            selectedPlates.forEach((input) =>
              selectedPlatesArr.push(input.value)
            );

            selectedPlatesArr.forEach((plateMaterial, i) => {
              if (!propertyParamsArr[i]) propertyParamsArr.push({});

              propertyParamsArr[i].plateMaterial = plateMaterial
                ? plateMaterial
                : null;
            });
          }

          // spacerProperty
          if (Object.values(propertyData)[0].spacerProperty) {
            const selectedSpacers = document.querySelectorAll(
              `#select__spacer--${lineName.toLowerCase()}`
            );

            selectedSpacers.forEach((input) =>
              selectedSpacersArr.push(input.value)
            );

            selectedSpacersArr.forEach((spacerMaterial, i) => {
              if (!propertyParamsArr[i]) propertyParamsArr.push({});

              propertyParamsArr[i].spacerMaterial = spacerMaterial
                ? spacerMaterial
                : null;
            });
          }

          selectedActivitiesArr.forEach((_, i) => {
            if (!linesData[i]) linesData.push({ lines: [] });

            linesData[i].lines.push({
              name: lineName,
              phaseActivity: selectedActivitiesArr[i],
              propertyParams: propertyParamsArr[i],
              comment: commentsArr[i],
            });
          });
        } else {
          const selectedActivityValue =
            document.querySelector(
              `#select__activity--${lineName.toLowerCase()}`
            ).value === 'true';

          let propertyParams = {};

          console.log(this.taskType);

          // boundaryCondition
          if (Object.values(propertyData)[0].boundaryCondition) {
            if (this.taskType === 'elasticity') {
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
            ).find(
              (charData) => Object.keys(charData)[0] === selectedPlateValue
            );

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
        }
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
      if (this.taskType === 'nonlinearity') {
        // NOTE: filling stage data: nonlinearity

        // Parameters
        const phaseIdInputs = document.querySelectorAll('#input__phase-id');
        const startFromPhaseInputs =
          document.querySelectorAll('#input__start-from');

        // Parameters of plastic calculation
        const calcTypeInput = document.querySelector('#select__calc-type');
        const selectDisplacement = document.querySelectorAll(
          '#select__displacement'
        );

        // Parameters of numerical calculation
        const maxStepsInputs = document.querySelectorAll('#input__max-steps');
        const toleratedErrorInputs = document.querySelectorAll(
          '#input__tolerated-error'
        );
        const maxUnloadingStepsInputs = document.querySelectorAll(
          '#input__max-unloading-steps'
        );
        const maxLoadFractionInputs = document.querySelectorAll(
          '#input__max-load-fraction'
        );
        const maxNumIterationInputs = document.querySelectorAll(
          '#input__max-num-iteration'
        );
        const desiredMinNumInputs = document.querySelectorAll(
          '#input__desired-min-number'
        );
        const desiredMaxNumInputs = document.querySelectorAll(
          '#input__desired-max-number'
        );

        let nonlinearityStageData = [];

        soilsData.forEach((_, i) => {
          if (i === 0) {
            nonlinearityStageData.push({
              id: 'Initial phase',
              data: {
                soils: soilsData[i].soils,
                lines: linesData[i].lines,
              },
            });
          } else {
            nonlinearityStageData.push({
              id: `Phase ${i}`,
              data: {
                soils: soilsData[i].soils,
                lines: linesData[i].lines,
              },
            });
          }
        });

        nonlinearityStageData.forEach((_, i) => {
          if (i === 0) {
            nonlinearityStageData[i].id = 'Initial phase';
            nonlinearityStageData[i].startFromPhase = null;
            nonlinearityStageData[i].deformationControlParameters = {
              resetDisplacementToZero: selectDisplacement[i].value === 'true',
              calculationType: calcTypeInput.value,
            };
            nonlinearityStageData[i].numericalControlParameters = {
              maxSteps: Number(maxStepsInputs[i].value),
              toleratedError: Number(toleratedErrorInputs[i].value),
              maxUnloadingSteps: Number(maxUnloadingStepsInputs[i].value),
              maxLoadFractionPerStep: Number(maxLoadFractionInputs[i].value),
              maxNumberOfIterations: Number(maxNumIterationInputs[i].value),
              desiredMinNumberOfIterations: Number(
                desiredMinNumInputs[i].value
              ),
              desiredMaxNumberOfIterations: Number(
                desiredMaxNumInputs[i].value
              ),
            };
          } else {
            nonlinearityStageData[i].id = phaseIdInputs[i - 1].value;
            nonlinearityStageData[i].startFromPhase =
              startFromPhaseInputs[i - 1].value;
            nonlinearityStageData[i].deformationControlParameters = {
              resetDisplacementToZero: selectDisplacement[i].value === 'true',
            };
            nonlinearityStageData[i].numericalControlParameters = {
              maxSteps: Number(maxStepsInputs[i].value),
              toleratedError: Number(toleratedErrorInputs[i].value),
              maxUnloadingSteps: Number(maxUnloadingStepsInputs[i].value),
              maxLoadFractionPerStep: Number(maxLoadFractionInputs[i].value),
              maxNumberOfIterations: Number(maxNumIterationInputs[i].value),
              desiredMinNumberOfIterations: Number(
                desiredMinNumInputs[i].value
              ),
              desiredMaxNumberOfIterations: Number(
                desiredMaxNumInputs[i].value
              ),
            };
          }
        });

        this.sendStageData({ stageData: {} });
        this.sendStageData({ stageData: nonlinearityStageData });
      } else if (
        this.taskType === 'filtration' ||
        this.taskType === 'temperature'
      ) {
        // console.log(this.rawStageData);
        this.sendStageData({ stageData: {} });
        this.sendStageData({ stageData: this.rawStageData });
      } else {
        initialStageData.Initial_phase = this.rawStageData;
        this.sendStageData({ stageData: {} });
        this.sendStageData({ stageData: initialStageData });
      }

      this.rawStageData = {
        soils: [],
        lines: [],
      };

      console.log('stageData');
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
};
</script>

<style scoped>
#fig01 {
  transform: translateX(-13%);
}

select,
option {
  font-family: inherit;
}

.btn__container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}

.add__phase {
  justify-self: center;
  grid-column: 2 / 3;
}

.apply_stage {
  grid-column: 3 / 4;
  justify-self: flex-end;
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
