<template>
  <section>
    <h1 class="bubble">Этап 2. Назначение расчетных свойств</h1>
    <the-figure figure-name="fig01"></the-figure>
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
    ...mapGetters(['gmshData', 'linesData', 'polygonsData', 'propertiesData']),
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
    if (Object.values(this.propertiesData).length === 0) {
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

      // NOTE: properties reset
      const plateProperties = document.querySelectorAll('#plate-property');
      const loadProperties = document.querySelectorAll('#load-property');
      const spacerProperties = document.querySelectorAll('#spacer-property');
      const boundaryConditionProperties = document.querySelectorAll(
        '#boundary-condition-property'
      );

      plateProperties.forEach((property) => {
        if (property.checked) property.checked = false;
      });
      loadProperties.forEach((property) => {
        if (property.checked) property.checked = false;
      });
      spacerProperties.forEach((property) => {
        if (property.checked) property.checked = false;
      });
      boundaryConditionProperties.forEach((property) => {
        if (property.checked) property.checked = false;
      });
    }
  },
};
</script>

<style scoped>
#fig01 {
  transform: translateX(-38%);
}
</style>
