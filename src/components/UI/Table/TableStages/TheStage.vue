<template>
  <button class="bubble btn">{{ stageName }}</button>
  <soil-table :two-dim-data="twoDimData"></soil-table>
  <line-table :one-dim-data="oneDimData"></line-table>
  <!-- <point-table></point-table> -->
</template>

<script>
import SoilTable from './SoilTable.vue';
import LineTable from './LineTable.vue';
// import PointTable from './PointTable.vue';

import { mapGetters } from 'vuex';

export default {
  components: {
    SoilTable,
    LineTable,
    // PointTable,
  },
  data() {
    return {
      twoDimData: null,
      oneDimData: null,
    };
  },
  props: ['stageName'],
  computed: {
    ...mapGetters(['characteristicsData']),
  },
  beforeMount() {
    this.twoDimData = this.characteristicsData.twoDimData;
    this.oneDimData = this.characteristicsData.oneDimData;
    // console.log(this.twoDimData);
    // console.log(this.oneDimData);
  },
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
