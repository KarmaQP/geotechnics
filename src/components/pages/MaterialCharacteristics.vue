<template>
  <section>
    <h1 class="bubble">Этап 3. Назначение характеристик материалов</h1>
    <table-characteristics
      :lines-data="linesData"
      :polygons-data="polygonsData"
    ></table-characteristics>
  </section>
</template>

<script>
import TableCharacteristics from '../UI/TableCharacteristics.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    TableCharacteristics,
  },
  computed: {
    ...mapGetters(['linesData', 'polygonsData']),
  },
};
</script>
