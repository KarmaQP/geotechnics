<template>
  <div class="point-element">
    <div class="tr">
      <div class="td">{{ pointName }}</div>
      <div class="td">{{ materialColor }}</div>
      <div class="td">
        <select>
          <option value="yes">Да</option>
          <option value="no">Нет</option>
        </select>
      </div>
      <div class="td">
        <input type="text" name="" id="" placeholder="Введите текст" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['pointName', 'materialColor'],
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
