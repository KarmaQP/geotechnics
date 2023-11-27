<template>
  <div class="generated-table table--1d-point">
    <div class="tr">
      <div class="td">{{ materialName }}</div>
      <div class="tr tr--multi-row">
        <div class="td">Модуль упругости, кПа</div>
        <div class="td">Площадь сечения, м&sup2;</div>
      </div>
      <div class="tr tr--multi-row">
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['materialName'],
};
</script>

<style scoped>
.tr {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
.tr--multi-row {
  display: flex;
  flex-direction: column;
}
</style>
