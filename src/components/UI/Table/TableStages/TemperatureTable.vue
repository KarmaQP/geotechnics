<template>
  <div class="table" v-if="taskType === 'temperature'">
    <div class="tr two-cols">
      <div class="th">Параметр</div>
      <div class="th">Величина</div>
    </div>
    <div class="generated-table">
      <div class="tr two-cols">
        <div class="td">Время расчета, с</div>
        <div class="td">
          <input
            type="number"
            id="input__calc-time"
            placeholder="Введите время..."
          />
        </div>
      </div>
    </div>
    <div class="generated-table">
      <div class="tr two-cols">
        <div class="td">Кол-во шагов интегрирования по времени</div>
        <div class="td">
          <input
            type="number"
            id="input__num-steps"
            placeholder="Введите количество шагов..."
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['taskType']),
  },
};
</script>
