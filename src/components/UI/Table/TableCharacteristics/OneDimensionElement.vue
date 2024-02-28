<template>
  <div class="generated-table table--1d">
    <div class="tr">
      <div class="td td--header">
        <div class="line-row" @click="toggleInfo">
          <input
            type="text"
            :id="`one-dim__name-${id}`"
            placeholder="Введите название..."
          />
        </div>
        <div>
          <i class="fa-solid" :class="arrowState" @click="toggleInfo"></i>
        </div>
      </div>
      <div class="tr tr--multi-row" v-show="infoShow">
        <div class="td">Удельный вес, кН/м&sup3;</div>
        <div class="td">Коэффициент Пуассона</div>
        <div class="td">Модуль упругости, кПа</div>
        <div class="td">Площадь сечения, м&sup2;</div>
        <div class="td">Момент инерции, м&#8308;</div>
        <div class="td">Выбрать тип работы:</div>
      </div>
      <div class="tr tr--multi-row" v-show="infoShow">
        <div class="td">
          <input
            type="number"
            :id="`one-dim__weight-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td">
          <input
            type="number"
            :id="`one-dim__poisson-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td">
          <input
            type="number"
            :id="`elastic-modulus-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td">
          <input
            type="number"
            :id="`sectional-area-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td">
          <input
            type="number"
            :id="`inertia-moment-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td td--select">
          <select :id="`work-type-${id}`">
            <option value="stretching-compression">Растяжение/сжатие</option>
            <option value="stretching-compression-bending">
              Растяжение/сжатие/изгиб
            </option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['id'],
  data() {
    return {
      infoShow: false,
    };
  },
  computed: {
    arrowState() {
      if (this.infoShow) return 'fa-chevron-down';
      else return 'fa-chevron-right';
    },
  },
  methods: {
    // NOTE: handling row and arrow click
    toggleInfo() {
      this.infoShow = !this.infoShow;
    },
  },
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

.td--header {
  display: flex;
  justify-content: space-between;
}

.td--header i {
  cursor: pointer;
  min-width: 5%;
}

.td--checkbox-container {
  text-align: center;
}

.line-row {
  min-width: 96%;
  cursor: pointer;
}

.td--select {
  padding: 0;
}

select,
option {
  font-family: inherit;
}
</style>
