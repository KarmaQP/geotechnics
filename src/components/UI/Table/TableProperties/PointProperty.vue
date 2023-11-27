<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ pointName }}</div>
      <div class="td">
        <div class="tr">
          <div class="td">- Точечная нагрузка</div>
          <div class="td">
            <select>
              <option value="yes">Да</option>
              <option value="no">Нет</option>
            </select>
          </div>
        </div>
        <div class="tr">
          <div class="td">- Одноузловой анкер</div>
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
  props: ['pointName', 'pointLoad', 'singleNodeAnchor'],
};
</script>
