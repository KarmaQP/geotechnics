<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Point)</div>
      <div class="th">Материал</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Примечание</div>
    </div>
    <the-point
      point-name="Point_1"
      material-color="Фиолетовый"
      class="light"
    ></the-point>
    <the-point
      point-name="Point_2"
      material-color="Красный"
      class="very-light"
    ></the-point>
  </div>
</template>

<script>
import ThePoint from './elements/ThePoint.vue';

export default {
  components: {
    ThePoint,
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
