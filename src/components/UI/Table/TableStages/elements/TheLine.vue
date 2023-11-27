<template>
  <div class="line-element">
    <div class="tr">
      <div class="td">{{ lineName }}</div>
      <div class="td">{{ materialColor }}</div>
      <div class="td">
        <select>
          <option value="yes">Да</option>
          <option value="no">Нет</option>
        </select>
      </div>
      <div class="td">
        <p>Нагрузка</p>
        <p>Граничное условие</p>
        <select>
          <option value="plate">Плита</option>
          <option value="balk">Балка</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['lineName', 'materialColor'],
};
</script>

<style scoped>
.light .tr {
  background-color: var(--light-blue-bg-color);
}

.very-light .tr {
  background-color: var(--very-light-blue-bg-color);
}
</style>
