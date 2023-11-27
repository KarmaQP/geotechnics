<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование объекта</div>
      <div class="th">Назначение свойств</div>
    </div>
    <polygon-property
      polygon-name="Polygon_1"
      property-name="Материал"
    ></polygon-property>
    <line-property
      line-name="Line_1"
      :plate-property="true"
      :load-property="false"
      :spacer-property="false"
      :boundary-condition-property="true"
    ></line-property>
    <line-property
      line-name="Line_2"
      :plate-property="true"
      :load-property="false"
      :spacer-property="false"
      :boundary-condition-property="true"
    ></line-property>
    <line-property
      line-name="Line_3"
      :plate-property="true"
      :load-property="false"
      :spacer-property="false"
      :boundary-condition-property="true"
    ></line-property>
    <line-property
      line-name="Line_4"
      :plate-property="true"
      :load-property="false"
      :spacer-property="false"
      :boundary-condition-property="true"
    ></line-property>
    <point-property
      point-name="Point_1"
      :point-load="true"
      :single-node-anchor="false"
    ></point-property>
    <point-property
      point-name="Point_2"
      :point-load="true"
      :single-node-anchor="false"
    ></point-property>
  </div>
</template>

<script>
import PolygonProperty from './Table/TableProperties/PolygonProperty.vue';
import LineProperty from './Table/TableProperties/LineProperty.vue';
import PointProperty from './Table/TableProperties/PointProperty.vue';

export default {
  components: {
    PolygonProperty,
    LineProperty,
    PointProperty,
  },
};
</script>

<style scoped>
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: 1fr 2fr;
}
</style>
