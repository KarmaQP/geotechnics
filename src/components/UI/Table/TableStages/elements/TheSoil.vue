<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ soilName }}</div>
      <div class="td">
        <select :id="`select__material--${soilName.toLowerCase()}`">
          <option value="null"></option>
          <option
            v-for="name in characteristicsNames"
            :key="name"
            :value="name"
          >
            {{ name }}
          </option>
        </select>
      </div>
      <div class="td">
        <select :id="`select__activity--${soilName.toLowerCase()}`">
          <option :value="true">Да</option>
          <option selected :value="false">Нет</option>
        </select>
      </div>
      <div class="td">
        <input
          type="text"
          :id="`input__comment--${soilName.toLowerCase()}`"
          placeholder="Введите текст..."
        />
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
