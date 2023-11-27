<template>
  <div class="generated-table table--2d">
    <div class="tr">
      <div class="td">{{ materialName }}</div>
      <div class="tr tr--multi-row">
        <div class="td">Удельный вес, кН/м&#179;</div>
        <div class="td">Коэффициент Пуассона</div>
      </div>
      <div class="tr tr--multi-row">
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
        <div class="td">
          <input type="number" name="" id="" placeholder="Введите значение" />
        </div>
      </div>
    </div>
    <div class="tr">
      <div class="td"></div>
      <div class="td td--h">Механические параметры</div>
      <div class="td"></div>
    </div>
    <div class="tr">
      <div class="td"></div>
      <div class="td td--h">
        <select @change="changeCurrentParameter($event)" name="" id="">
          <option value="linear_elastic">Linear elastic</option>
          <option value="mohr-coloumb">Mohr-coloumb</option>
          <option value="modify_cam-clay">Modify cam-clay</option>
        </select>
      </div>
      <div class="td"></div>
    </div>
    <div v-if="selectedParameter === 'linear_elastic'" class="tr">
      <div class="td"></div>
      <div class="td">Модуль упругости, кПа</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'mohr-coloumb'" class="tr">
      <div class="td"></div>
      <div class="td">Модуль упругости, кПа</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'mohr-coloumb'" class="tr">
      <div class="td"></div>
      <div class="td">Угол внутреннего трения, град</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'mohr-coloumb'" class="tr">
      <div class="td"></div>
      <div class="td">Удельное сцепление, кПа</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'mohr-coloumb'" class="tr">
      <div class="td"></div>
      <div class="td">Угол дилатансии, град</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'mohr-coloumb'" class="tr">
      <div class="td"></div>
      <div class="td">Прочность на растяжение, кПа</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'modify_cam-clay'" class="tr">
      <div class="td"></div>
      <div class="td">Индекс компрессии</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'modify_cam-clay'" class="tr">
      <div class="td"></div>
      <div class="td">Индекс рекомпрессии</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
    <div v-if="selectedParameter === 'modify_cam-clay'" class="tr">
      <div class="td"></div>
      <div class="td">Mcsl</div>
      <div class="td">
        <input type="number" name="" id="" placeholder="Введите значение" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['materialName'],
  data() {
    return {
      selectedParameter: 'linear_elastic',
    };
  },
  methods: {
    changeCurrentParameter(event) {
      this.selectedParameter = event.target.value;
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
</style>
