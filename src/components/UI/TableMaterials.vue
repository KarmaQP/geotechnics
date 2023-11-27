<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование объекта</div>
      <div class="th">Цвет</div>
      <div class="th">Комментарий</div>
      <div class="th">Примечание</div>
    </div>
    <the-material
      material-name="Материал 1"
      material-color="Серый"
      material-comment="Комментарий к материалу 1"
      material-note="Примечание к материалу 2"
    ></the-material>
    <the-material
      material-name="Материал 2"
      material-color="Розовый"
      material-comment="Комментарий к материалу 2"
      material-note="Примечание к материалу 2"
    ></the-material>
  </div>
</template>

<script>
import TheMaterial from './Table/TableMaterials/TheMaterial.vue';

export default {
  components: {
    TheMaterial,
  },
};
</script>

<style scoped>
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}
/* .tr:nth-child(even) {
  background-color: var(--light-blue-bg-color);
}
.tr:nth-child(odd) {
  background-color: var(--very-light-blue-bg-color);
} */
</style>
