<template>
  <div class="properties-container">
    <div class="table">
      <div class="tr">
        <div class="th">Наименование объекта</div>
        <div class="th">Назначение свойств</div>
      </div>
      <div class="generated-table">
        <div class="toggle-container">
          <div @click="togglePolygons">
            {{ polygonsLabel }} полигоны (размер: {{ polygonsData.length }})
          </div>
          <i
            class="fa-solid"
            :class="polygonsArrowState"
            @click="togglePolygons"
          ></i>
        </div>
      </div>
      <polygon-property
        v-for="polygonData in polygonsData"
        v-show="showPolygons"
        :key="polygonData[0]"
        :polygon-name="polygonData[0]"
      ></polygon-property>
      <div class="generated-table">
        <div class="toggle-container">
          <div @click="toggleLines">
            {{ linesLabel }} линии (размер: {{ linesData.length }})
          </div>
          <i class="fa-solid" :class="linesArrowState" @click="toggleLines"></i>
        </div>
      </div>
      <line-property
        v-for="lineData in linesData"
        v-show="showLines"
        :key="lineData[0]"
        :line-name="lineData[0]"
      ></line-property>
    </div>
    <button type="button" @click="applyProperties">Применить свойства</button>
  </div>
</template>

<script>
import PolygonProperty from './Table/TableProperties/PolygonProperty.vue';
import LineProperty from './Table/TableProperties/LineProperty.vue';
// import PointProperty from './Table/TableProperties/PointProperty.vue';
import axios from 'axios';

import { mapActions } from 'vuex';
import { mapGetters } from 'vuex';

export default {
  components: {
    PolygonProperty,
    LineProperty,
    // PointProperty,
  },
  props: ['polygonsData', 'linesData'],
  data() {
    return {
      showPolygons: false,
      showLines: false,
    };
  },
  computed: {
    ...mapGetters(['propertiesData']),
    linesArrowState() {
      if (this.showLines) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
    polygonsArrowState() {
      if (this.showPolygons) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
    linesLabel() {
      if (this.showLines) return 'Скрыть';
      else return 'Показать';
    },
    polygonsLabel() {
      if (this.showPolygons) return 'Скрыть';
      else return 'Показать';
    },
  },
  methods: {
    ...mapActions(['sendPropertiesData']),
    toggleLines() {
      this.showLines = !this.showLines;
    },
    togglePolygons() {
      this.showPolygons = !this.showPolygons;
    },
    async applyProperties() {
      let lData = [];
      let pData = [];

      const linesPlateProperties = document.querySelectorAll('#plate-property');
      const linesLoadProperties = document.querySelectorAll('#load-property');
      const linesSpacerProperties =
        document.querySelectorAll('#spacer-property');
      const linesBoundaryConditionProperties = document.querySelectorAll(
        '#boundary-condition-property'
      );

      this.linesData.forEach((lineData, i) => {
        lData.push({
          [lineData[0]]: {
            plateProperty: linesPlateProperties[i].checked,
            loadProperty: linesLoadProperties[i].checked,
            spacerProperty: linesSpacerProperties[i].checked,
            boundaryCondition: linesBoundaryConditionProperties[i].checked,
          },
        });
      });

      this.polygonsData.forEach((polygonData) => {
        pData.push({
          [polygonData[0]]: 'material',
        });
      });

      this.sendPropertiesData({
        propertiesData: {
          linesProperties: lData,
          polygonsProperties: pData,
        },
      });

      console.log(this.propertiesData);

      /* global $ */
      const formData = new FormData();
      const csrf = $('input[name=csrfmiddlewaretoken]').val();

      formData.append('propertiesData', JSON.stringify(this.propertiesData));
      formData.append('csrfmiddlewaretoken', csrf);

      const response = await axios.post('api/test/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response);
    },
  },
};
</script>

<style scoped>
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: 1fr 2fr;
}

i {
  cursor: pointer;
  min-width: 1%;
}

.toggle-container {
  font-weight: bold;
  padding: 0.8rem 0.4rem;
  display: flex;
  justify-content: space-between;
}

.toggle-container div {
  min-width: 98%;
  cursor: pointer;
}

.properties-container {
  text-align: right;
}

.table {
  text-align: left;
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
