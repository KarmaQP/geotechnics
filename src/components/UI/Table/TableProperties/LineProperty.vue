<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ lineName }}</div>
      <div class="td">
        <div class="tr">
          <div class="td">- Свойство плита</div>
          <div class="td">
            <select>
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойство нагрузка</div>
          <div class="td">
            <select>
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойство распорка</div>
          <div class="td">
            <select>
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойства граничное условие</div>
          <div class="td">
            <select>
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'lineName',
    'plateProperty',
    'loadProperty',
    'spacerProperty',
    'boundaryConditionProperty',
  ],
};
</script>
