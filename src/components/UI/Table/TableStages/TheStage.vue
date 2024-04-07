<template>
  <button class="bubble btn">{{ stageName }}</button>
  <init-table
    v-if="stageType === 'init' && taskType === 'nonlinearity'"
  ></init-table>
  <phase-table
    v-if="stageType === 'phase' && taskType === 'nonlinearity'"
  ></phase-table>
  <soil-table></soil-table>
  <line-table></line-table>
  <!-- <point-table></point-table> -->
</template>

<script>
import SoilTable from './SoilTable.vue';
import LineTable from './LineTable.vue';
import InitTable from './InitTable.vue';
import PhaseTable from './PhaseTable.vue';
// import PointTable from './PointTable.vue';

export default {
  props: ['stageName', 'stageType', 'taskType'],
  components: {
    SoilTable,
    LineTable,
    InitTable,
    PhaseTable,
    // PointTable,
  },
};
</script>

<style scoped>
.table {
  text-align: left;
}

/* .btn {
  font-size: 2rem;
  margin-top: 3.2rem;
}
.btn:first-child {
  margin-top: 0;
} */

.btn__container {
  text-align: right;
}

button {
  margin-top: 2.4rem;
  padding: 0.8rem;
  background-color: var(--blue-bg-color);
  color: var(--text-color);
  font-size: 1.4rem;
  transition: all 0.3s;
}

button:hover {
  background-color: var(--hover-blue-bg-color);
}

button:active {
  background-color: var(--active-blue-bg-color);
}
</style>
