<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Soil)</div>
      <div class="th">Материал</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Примечание</div>
    </div>
    <the-soil
      soil-name="Soil_1"
      material-color="Серый"
      class="light"
    ></the-soil>
    <the-soil
      soil-name="Soil_2"
      material-color="Белый"
      class="very-light"
    ></the-soil>
  </div>
</template>

<script>
import TheSoil from './elements/TheSoil.vue';

export default {
  components: {
    TheSoil,
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
