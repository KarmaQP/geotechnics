<template>
  <div class="generated-table table--2d">
    <div class="tr">
      <div class="td td--header">
        <div class="line-row" @click="toggleInfo">
          <input
            type="text"
            :id="`name-${id}`"
            placeholder="Введите название..."
          />
        </div>
        <div>
          <i class="fa-solid" :class="arrowState" @click="toggleInfo"></i>
        </div>
      </div>
      <div class="tr tr--multi-row" v-show="infoShow">
        <div class="td">Удельный вес, кН/м&#179;</div>
        <div class="td">Коэффициент Пуассона</div>
        <div class="td adv-params__label">Дополнительные параметры</div>
      </div>
      <div class="tr tr--multi-row" v-show="infoShow">
        <div class="td">
          <input
            type="number"
            :id="`weight-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td">
          <input
            type="number"
            :id="`poisson-${id}`"
            placeholder="Введите значение..."
          />
        </div>
        <div class="td adv-params">
          <div>
            <label>Фильтрация:</label>
            <input type="checkbox" />
          </div>
          <div>
            <label>Температура:</label>
            <input type="checkbox" />
          </div>
        </div>
      </div>
    </div>
    <div class="tr" v-show="infoShow">
      <div class="td"></div>
      <div class="td td--h">Механические параметры</div>
      <div class="td"></div>
    </div>
    <div class="tr" v-show="infoShow">
      <div class="td"></div>
      <div class="td td--h">
        <select
          @change="changeCurrentParameter($event)"
          :id="`mech-parameter-${id}`"
        >
          <option value="linear-elastic">Linear elastic</option>
          <option value="mohr-coloumb">Mohr-coloumb</option>
          <option value="cam-clay">Modify cam-clay</option>
        </select>
      </div>
      <div class="td"></div>
    </div>
    <div
      v-if="selectedParameter === 'linear-elastic'"
      v-show="infoShow"
      class="tr"
    >
      <div class="td"></div>
      <div class="td">Модуль упругости, кПа</div>
      <div class="td">
        <input
          type="number"
          :id="`linear-elastic-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div
      v-if="selectedParameter === 'mohr-coloumb'"
      v-show="infoShow"
      class="tr"
    >
      <div class="td"></div>
      <div class="td">Модуль упругости, кПа</div>
      <div class="td">
        <input
          type="number"
          :id="`mohr-coloumb-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div
      v-if="selectedParameter === 'mohr-coloumb'"
      v-show="infoShow"
      class="tr"
    >
      <div class="td"></div>
      <div class="td">Угол внутреннего трения, град</div>
      <div class="td">
        <input
          type="number"
          :id="`mohr-coloumb-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div
      v-if="selectedParameter === 'mohr-coloumb'"
      v-show="infoShow"
      class="tr"
    >
      <div class="td"></div>
      <div class="td">Удельное сцепление, кПа</div>
      <div class="td">
        <input
          type="number"
          :id="`mohr-coloumb-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div
      v-if="selectedParameter === 'mohr-coloumb'"
      v-show="infoShow"
      class="tr"
    >
      <div class="td"></div>
      <div class="td">Угол дилатансии, град</div>
      <div class="td">
        <input
          type="number"
          :id="`mohr-coloumb-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div
      v-if="selectedParameter === 'mohr-coloumb'"
      v-show="infoShow"
      class="tr"
    >
      <div class="td"></div>
      <div class="td">Прочность на растяжение, кПа</div>
      <div class="td">
        <input
          type="number"
          :id="`mohr-coloumb-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div v-if="selectedParameter === 'cam-clay'" v-show="infoShow" class="tr">
      <div class="td"></div>
      <div class="td">Индекс компрессии</div>
      <div class="td">
        <input
          type="number"
          :id="`cam-clay-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div v-if="selectedParameter === 'cam-clay'" v-show="infoShow" class="tr">
      <div class="td"></div>
      <div class="td">Индекс рекомпрессии</div>
      <div class="td">
        <input
          type="number"
          :id="`cam-clay-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
    <div v-if="selectedParameter === 'cam-clay'" v-show="infoShow" class="tr">
      <div class="td"></div>
      <div class="td">Mcsl</div>
      <div class="td">
        <input
          type="number"
          :id="`cam-clay-${id}`"
          placeholder="Введите значение..."
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['id'],
  data() {
    return {
      selectedParameter: 'linear-elastic',
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
    changeCurrentParameter(event) {
      this.selectedParameter = event.target.value;
    },
    // NOTE: handling row and arrow click
    toggleInfo() {
      this.infoShow = !this.infoShow;
    },
  },
};
</script>

<style scoped>
.tr {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
.tr--multi-row {
  display: flex;
  flex-direction: column;
}
.generated-table .tr .td:first-child {
  border: none;
  border-right: 1px solid #fff;
}
.generated-table .tr:first-child {
  border-top: 1px solid #fff;
}
.generated-table .tr:last-child {
  border-bottom: 1px solid #fff;
}
select {
  color: var(--text-color);
  background-color: var(--blue-bg-color);
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

/* .adv-params {
  display: flex;
  justify-content: space-between;
  align-items: center;
} */

.adv-params div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.4rem;
}

.adv-params__label {
  min-height: 100%;
}
</style>
