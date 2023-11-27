<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ polygonName }}</div>
      <div class="td">{{ propertyName }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['polygonName', 'propertyName'],
};
</script>
