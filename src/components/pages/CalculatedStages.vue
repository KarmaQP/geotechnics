<template>
  <section>
    <h1 class="bubble">Этап 4. Создание расчетных этапов</h1>
    <the-figure figure-name="fig01"></the-figure>
    <tables-stage></tables-stage>
  </section>
</template>

<script>
import TablesStage from '../UI/TablesStage.vue';
import { mapGetters } from 'vuex';

/* global mpld3 */

export default {
  components: {
    TablesStage,
  },
  computed: {
    ...mapGetters(['gmshData']),
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

    // const polygonsData = this.polygonsData;
    // const linesData = this.linesData;

    // polygonsData.forEach((polygon) => {
    //   console.log(toRaw(polygon));
    // });
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
.btn {
  font-size: 2rem;
}
#fig01 {
  transform: translateX(-38%);
}
</style>
