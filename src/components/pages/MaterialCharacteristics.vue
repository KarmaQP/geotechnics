<template>
  <section>
    <h1 class="bubble">Этап 3. Назначение характеристик материалов</h1>
    <the-figure figure-name="fig01"></the-figure>
    <table-characteristics></table-characteristics>
  </section>
</template>

<script>
import TableCharacteristics from '../UI/TableCharacteristics.vue';
import { mapGetters } from 'vuex';

/* global mpld3 */

export default {
  components: {
    TableCharacteristics,
  },
  computed: {
    ...mapGetters(['gmshData', 'linesData', 'polygonsData']),
  },
  mounted() {
    if (this.gmshData === null) return;

    mpld3.draw_figure('fig01', this.gmshData);

    const legend = document.querySelector('.mpld3-staticpaths');
    Array.from(legend.children).forEach((child, i) => {
      if (i === 0) child.remove();
      if (i > 0) {
        Array.from(child.children).forEach((circle, j) => {
          if (j < 2) circle.remove();
        });
      }
    });
  },
  updated() {
    const fig = document.querySelector('#fig01');
    fig.innerHTML = '';

    mpld3.draw_figure('fig01', this.gmshData);

    const legend = document.querySelector('.mpld3-staticpaths');
    Array.from(legend.children).forEach((child, i) => {
      if (i === 0) child.remove();
      if (i > 0) {
        Array.from(child.children).forEach((circle, j) => {
          if (j < 2) circle.remove();
        });
      }
    });
  },
};
</script>

<style scoped>
#fig01 {
  transform: translateX(-38%);
}
</style>
