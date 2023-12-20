<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ soilName }}</div>
      <div class="td">
        <select>
          <option value="null"></option>
          <option v-for="name in characteristicsNames" :key="name" value="name">
            {{ name }}
          </option>
        </select>
      </div>
      <div class="td">
        <select>
          <option value="yes">Да</option>
          <option value="no">Нет</option>
        </select>
      </div>
      <div class="td">
        <input type="text" name="" id="" placeholder="Введите текст..." />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['soilName', 'twoDimData'],
  data() {
    return {
      characteristicsNames: [],
    };
  },
  beforeMount() {
    this.twoDimData.forEach((data) => {
      this.characteristicsNames.push(Object.entries(data)[0][0]);
    });
  },
};
</script>
