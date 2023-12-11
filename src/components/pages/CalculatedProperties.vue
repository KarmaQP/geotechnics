<template>
  <section>
    <h1 class="bubble">Этап 2. Назначение расчетных свойств</h1>
    <the-figure></the-figure>
    <table-properties
      :lines-data="linesData"
      :polygons-data="polygonsData"
    ></table-properties>
  </section>
</template>

<script>
import TableProperties from '../UI/TableProperties.vue';

// import { mapActions } from 'vuex';
import { mapGetters } from 'vuex';

/* global mpld3 */

export default {
  components: {
    TableProperties,
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
          console.log(j, circle);
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
};
</script>
