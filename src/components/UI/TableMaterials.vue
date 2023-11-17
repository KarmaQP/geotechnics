<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование объекта</div>
      <div class="th">Цвет</div>
      <div class="th">Комментарий</div>
      <div class="th">Примечание</div>
    </div>
    <div class="tr">
      <div class="td">Материал 1</div>
      <div class="td">Серый</div>
      <div class="td">Этот грунт нужно будет выключить</div>
      <div class="td">-</div>
    </div>
    <div class="tr">
      <div class="td">Материал 2</div>
      <div class="td">Розовый</div>
      <div class="td">Это действительно розовый грунт</div>
      <div class="td">Примечание к материалу 2</div>
    </div>
  </div>
</template>

<style scoped>
.table {
  margin-top: 3.2rem;
  min-width: 100%;
  background-color: #ccc;
}
.tr {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}
.th,
.td {
  padding: 0.4rem;
  line-height: 1.2;
  border: 1px solid #fff;
}
.th {
  background-color: var(--blue-bg-color);
  color: var(--text-color);
  font-size: 1.6rem;
}
.tr:nth-child(even) {
  background-color: var(--light-blue-bg-color);
}
.tr:nth-child(odd) {
  background-color: var(--very-light-blue-bg-color);
}
</style>
