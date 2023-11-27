<template>
  <div class="table">
    <div class="tr tr--header">
      <div class="th">Наименование объекта</div>
      <div class="th">Общие параметры</div>
      <div class="th">Значение</div>
    </div>
    <two-dimensions material-name="Материал 1"></two-dimensions>
    <two-dimensions material-name="Материал 2"></two-dimensions>
    <one-dimension-element
      material-name="Материал 1 линия"
    ></one-dimension-element>
    <one-dimension-element
      material-name="Материал 2 линия"
    ></one-dimension-element>
    <one-dimension-element
      material-name="Материал 3 линия"
    ></one-dimension-element>
    <one-dimension-element
      material-name="Материал 4 линия"
    ></one-dimension-element>
    <one-dimension-point material-name="Материал 1 точка"></one-dimension-point>
    <one-dimension-point material-name="Материал 2 точка"></one-dimension-point>
    <one-dimension-point material-name="Материал 3 точка"></one-dimension-point>
  </div>
</template>

<script>
import TwoDimensions from './Table/TableCharacteristics/TwoDimensions.vue';
import OneDimensionElement from './Table/TableCharacteristics/OneDimensionElement.vue';
import OneDimensionPoint from './Table/TableCharacteristics/OneDimensionPoint.vue';

export default {
  components: {
    TwoDimensions,
    OneDimensionElement,
    OneDimensionPoint,
  },
};
</script>

<style scoped>
.tr {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
</style>
