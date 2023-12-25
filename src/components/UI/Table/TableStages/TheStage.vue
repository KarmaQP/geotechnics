<template>
  <button class="bubble btn">{{ stageName }}</button>
  <soil-table :two-dim-data="twoDimData"></soil-table>
  <line-table :one-dim-data="oneDimData"></line-table>
  <button type="button" class="btn bubble" @click="applyStage">
    Применить
  </button>
  <!-- <point-table></point-table> -->
</template>

<script>
import SoilTable from './SoilTable.vue';
import LineTable from './LineTable.vue';
// import PointTable from './PointTable.vue';

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
      stageData: {
        soils: [],
        lines: [],
      },
    };
  },
  props: ['stageName'],
  computed: {
    ...mapGetters([
      'characteristicsData',
      'propertiesData',
      'linesData',
      'polygonsData',
    ]),
  },
  methods: {
    applyStage() {
      // NOTE: filling stage data: soils
      this.propertiesData.polygonsProperties.forEach((propertyData) => {
        const [soilName] = [...Object.keys(propertyData)];

        const selectMaterialValue = document.querySelector(
          `#select__material--${soilName.toLowerCase()}`
        ).value;
        const selectedMaterial = Object.values(this.twoDimData).find(
          (charData) => Object.keys(charData)[0] === selectMaterialValue
        );

        const selectedActivityValue =
          document.querySelector(`#select__activity--${soilName.toLowerCase()}`)
            .value === 'true';

        const comment = document.querySelector(
          `#input__comment--${soilName.toLowerCase()}`
        ).value;

        this.stageData.soils.push({
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

        // boundaryCondition
        if (Object.values(propertyData)[0].boundaryCondition) {
          const uxValue = Number(
            document.querySelector(`#input__bound-x--${lineName.toLowerCase()}`)
              .value
          );
          const uyValue = Number(
            document.querySelector(`#input__bound-y--${lineName.toLowerCase()}`)
              .value
          );

          propertyParams.ux = uxValue;
          propertyParams.uy = uyValue;
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
          const selectedMaterial = Object.values(this.oneDimData).find(
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
          const selectedMaterial = Object.values(this.oneDimData).find(
            (charData) => Object.keys(charData)[0] === selectedSpacerValue
          );

          propertyParams.spacerMaterial = selectedMaterial
            ? selectedMaterial
            : null;
        }

        const comment = document.querySelector(
          `#input__comment--${lineName.toLowerCase()}`
        ).value;

        this.stageData.lines.push({
          name: lineName,
          phaseActivity: selectedActivityValue,
          propertyParams: propertyParams,
          comment: comment,
        });
      });

      console.log(this.stageData);
    },
  },
  beforeMount() {
    this.twoDimData = this.characteristicsData.twoDimData;
    this.oneDimData = this.characteristicsData.oneDimData;
  },
};
</script>

<style scoped>
.table {
  margin-top: 3.2rem;
}
.btn {
  font-size: 2rem;
  margin-top: 3.2rem;
}
.btn:first-child {
  margin-top: 0;
}
</style>
