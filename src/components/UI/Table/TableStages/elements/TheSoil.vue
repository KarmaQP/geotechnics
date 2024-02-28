<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ soilName }}</div>
      <div class="td">
        <select
          class="select__material"
          :id="`select__material--${soilName.toLowerCase()}`"
        >
          <option value="null"></option>
          <option
            v-for="obj in characteristicsData.twoDimData"
            :key="Object.keys(obj)[0]"
            :value="Object.keys(obj)[0]"
          >
            {{ Object.keys(obj)[0] }}
          </option>
        </select>
      </div>
      <div class="td">
        <select :id="`select__activity--${soilName.toLowerCase()}`">
          <option selected :value="true">Да</option>
          <option :value="false">Нет</option>
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
import { mapGetters } from 'vuex';

export default {
  props: ['soilName'],
  computed: {
    ...mapGetters(['characteristicsData']),
  },
};
</script>

<style scoped>
select,
option {
  font-family: inherit;
}
</style>
