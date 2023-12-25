<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Line)</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Параметры свойств</div>
      <div class="th">Примечание</div>
    </div>
    <the-line
      v-for="line in Object.entries(newLinesData)"
      :key="line[0]"
      :one-dim-data="oneDimData"
      :property-data="line"
    ></the-line>
  </div>
</template>

<script>
import TheLine from './elements/TheLine.vue';

import { mapGetters } from 'vuex';

export default {
  components: {
    TheLine,
  },
  props: ['oneDimData'],
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
};
</script>

<style scoped>
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr 2fr;
}
</style>
