<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Line)</div>
      <div class="th">Параметры свойств</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Примечание</div>
    </div>
    <the-line
      v-for="lineProperty in propertiesData.linesProperties"
      :key="Object.keys(lineProperty)[0]"
      :property-data="lineProperty"
    ></the-line>
    <!-- <the-line
      v-for="line in Object.entries(newLinesData)"
      :key="line[0]"
      :one-dim-data="oneDimData"
      :property-data="line"
    ></the-line> -->
  </div>
</template>

<script>
import TheLine from './elements/TheLine.vue';

import { mapGetters } from 'vuex';

export default {
  components: {
    TheLine,
  },
  data() {
    return {
      newLinesData: [],
    };
  },
  computed: {
    ...mapGetters(['propertiesData', 'characteristicsData']),
  },
  beforeMount() {
    this.newLinesData = this.propertiesData.linesProperties;
  },
  updated() {
    this.newLinesData = this.propertiesData.linesProperties;
  },
};
</script>

<style scoped>
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: 1fr 2fr 0.8fr 2fr;
}
</style>
