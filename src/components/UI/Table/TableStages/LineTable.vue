<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Line)</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Параметры свойств</div>
      <div class="th">Примечания</div>
    </div>
    <the-line
      v-for="line in linesData"
      :key="line[0]"
      :line-name="line[0]"
      :one-dim-data="oneDimData"
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
  computed: {
    ...mapGetters(['linesData']),
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
