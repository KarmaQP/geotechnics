<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Soil)</div>
      <div class="th">Материал</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Примечание</div>
    </div>
    <the-soil
      v-for="polygon in polygonsData"
      :key="polygon[0]"
      :soil-name="polygon[0]"
      :two-dim-data="twoDimData"
    ></the-soil>
  </div>
</template>

<script>
import TheSoil from './elements/TheSoil.vue';

import { mapGetters } from 'vuex';

export default {
  components: {
    TheSoil,
  },
  props: ['twoDimData'],
  computed: {
    ...mapGetters(['polygonsData']),
  },
};
</script>

<style scoped>
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 2fr;
}
</style>
