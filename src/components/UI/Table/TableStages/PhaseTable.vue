<template>
  <div class="table">
    <div class="tr">
      <div class="th">Параметры</div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Название фазы</div>
        <div class="td">
          <input
            type="text"
            id="input__phase-id"
            placeholder="Введите название фазы..."
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Начинается после фазы</div>
        <div class="td">
          <input
            type="text"
            id="input__start-from"
            placeholder="Введите название фазы..."
          />
        </div>
      </div>
    </div>
    <div class="tr">
      <div class="th">Параметры пластического расчета</div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Обнуление накопленных перемещений</div>
        <div class="td">
          <select id="select__displacement">
            <option selected :value="true">Да</option>
            <option :value="false">Нет</option>
          </select>
        </div>
      </div>
    </div>
    <div class="tr">
      <div class="th">Параметры численного расчета</div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Максимальное количество шагов</div>
        <div class="td">
          <input
            type="number"
            id="input__max-steps"
            placeholder="Введите кол-во шагов..."
            value="1000"
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Погрешность расчета</div>
        <div class="td">
          <input
            type="number"
            id="input__tolerated-error"
            placeholder="Введите погрешность..."
            value="0.01"
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Максимальное количество шагов разгрузки</div>
        <div class="td">
          <input
            type="number"
            id="input__max-unloading-steps"
            placeholder="Введите кол-во шагов..."
            value="5"
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Доля приложения нагрузки на первом шаге</div>
        <div class="td">
          <input
            type="number"
            id="input__max-load-fraction"
            placeholder="Введите долю..."
            value="0.5"
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Максимальное количество итераций</div>
        <div class="td">
          <input
            type="number"
            id="input__max-num-iteration"
            placeholder="Введите кол-во итераций..."
            value="60"
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Предпочтительное минимальное количество итераций</div>
        <div class="td">
          <input
            type="number"
            id="input__desired-min-number"
            placeholder="Введите кол-во итераций..."
            value="5"
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr">
        <div class="td">Предпочтительное максимальное количество итераций</div>
        <div class="td">
          <input
            type="number"
            id="input__desired-max-number"
            placeholder="Введите кол-во итераций..."
            value="15"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tr {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.th {
  text-align: center;
  padding: 0.8rem 0;
}

.tr > .th {
  grid-column: 1 / 3;
}
</style>
