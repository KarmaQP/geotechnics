<template>
  <div class="generated-table table--1d">
    <div class="tr">
      <div class="td">{{ materialName }}</div>
      <div class="tr tr--multi-row">
        <div class="td">Удельный вес, кН/м&sup3;</div>
        <div class="td">Коэффициент Пуассона</div>
        <div class="td">Модуль упругости, кПа</div>
        <div class="td">Площадь сечения, м&sup2;</div>
        <div class="td">Момент инерции, м&#8308;</div>
        <div class="td">
          <p>Выбрать тип работы:</p>
          <p>1) Растяжение/сжатие</p>
          <p>1) Растяжение/сжатие/изгиб</p>
        </div>
      </div>
      <div class="tr tr--multi-row">
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['materialName'],
};
</script>

<style scoped>
.tr--multi-row .td:last-child {
  flex: 2;
}
.tr {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
.tr--multi-row {
  display: flex;
  flex-direction: column;
}
</style>
