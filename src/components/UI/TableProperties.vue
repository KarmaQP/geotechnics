<template>
  <div class="table">
    <div class="tr">
      <div class="th">Наименование объекта</div>
      <div class="th">Назначение свойств</div>
    </div>
    <div class="tr">
      <div class="td">Polygon_1</div>
      <div class="td">Материал</div>
    </div>
    <div class="tr">
      <div class="td">Line_1</div>
      <div class="td">
        <div class="tr">
          <div class="td">- Свойство плита</div>
          <div class="td">
            <select class="select--very-light">
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойство нагрузка</div>
          <div class="td">
            <select class="select--light">
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойство распорка</div>
          <div class="td">
            <select class="select--very-light">
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойства граничное условие</div>
          <div class="td">
            <select class="select--light">
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="tr">
      <div class="td">Point_1</div>
      <div class="td">
        <div class="tr">
          <div class="td">- Точечная нагрузка</div>
          <div class="td">
            <select class="select--very-light">
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Одноузловой анкер</div>
          <div class="td">
            <select class="select--light">
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tr .td .tr .td {
  border: none;
}
select {
  min-width: 100%;
}
.tr .td .tr .td:first-child {
  border-right: 1px solid #000;
}
.tr .td .tr {
  grid-template-columns: 2fr 1fr;
}
.table {
  margin-top: 3.2rem;
  min-width: 100%;
  background-color: #ccc;
}
.tr {
  display: grid;
  grid-template-columns: 1fr 2fr;
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
.tr:nth-child(even),
.select--light {
  background-color: var(--light-blue-bg-color);
}
.tr:nth-child(odd),
.select--very-light {
  background-color: var(--very-light-blue-bg-color);
}
</style>
