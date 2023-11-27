<template>
  <button class="bubble btn">{{ stageName }}</button>
  <soil-table></soil-table>
  <line-table></line-table>
  <point-table></point-table>
</template>

<script>
import SoilTable from './SoilTable.vue';
import LineTable from './LineTable.vue';
import PointTable from './PointTable.vue';

export default {
  components: {
    SoilTable,
    LineTable,
    PointTable,
  },
  props: ['stageName'],
};
</script>

<style scoped>
.table {
  margin-top: 3.2rem;
}
.btn {
  font-size: 2rem;
  margin-top: 3.2rem;
}
.btn:first-child {
  margin-top: 0;
}
</style>
