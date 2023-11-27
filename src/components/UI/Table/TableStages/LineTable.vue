<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование полигона (Line)</div>
      <div class="th">Материал</div>
      <div class="th">Активность на фазе</div>
      <div class="th">Свойства объектов</div>
    </div>
    <the-line
      line-name="Line_1"
      material-color="Синий"
      class="light"
    ></the-line>
    <the-line
      line-name="Line_2"
      material-color="Розовый"
      class="very-light"
    ></the-line>
  </div>
</template>

<script>
import TheLine from './elements/TheLine.vue';

export default {
  components: {
    TheLine,
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
