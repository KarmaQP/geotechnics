<template>
  <base-dialog
    v-if="isModalShown"
    title="Выберите нужные геометрические примитивы"
    @close="closeModal"
  >
    <template #default>
      <ul>
        <li v-for="lineData in linesData" :key="lineData[0]">
          <div class="list-item">
            <input
              id="line-data"
              name="line-data"
              type="checkbox"
              :value="lineData[0]"
            />
            <label for="line-data">{{ lineData[0] }}</label>
          </div>
        </li>
        <li v-for="polygonData in polygonsData" :key="polygonData[0]">
          <div class="list-item">
            <input
              id="polygon-data"
              name="polygon-data"
              type="checkbox"
              :value="polygonData[0]"
            />
            <label for="polygon-data">{{ polygonData[0] }}</label>
          </div>
        </li>
      </ul>
    </template>
    <template #action>
      <button type="button" @click="getSelectedPrimitives(selectedRowId)">
        Принять
      </button>
    </template>
  </base-dialog>
  <div class="table-container">
    <div class="table">
      <div class="tr">
        <div class="th">Наименование группы элементов</div>
        <div class="th">Цвет</div>
        <div class="th">Комментарий</div>
        <div class="th">Список геометрических примитивов</div>
      </div>
      <the-material
        v-for="i in countRows"
        :key="i"
        :id="i"
        :selected-primitives="geometricPrimitives[i - 1]"
        @toggle-modal="toggleModal"
      ></the-material>
    </div>
    <button @click="addRow"><i class="fa-solid fa-plus"></i></button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { isProxy, toRaw } from 'vue';
import TheMaterial from './Table/TableMaterials/TheMaterial.vue';

export default {
  components: {
    TheMaterial,
  },
  data() {
    return {
      countRows: 1,
      isModalShown: false,
      geometricPrimitives: [[]],
      selectedRowId: null,
    };
  },
  computed: {
    ...mapGetters(['linesData', 'polygonsData']),
  },
  methods: {
    addRow() {
      this.countRows++;
      this.geometricPrimitives.push([]);
    },
    toggleModal(id) {
      this.isModalShown = !this.isModalShown;
      this.selectedRowId = id - 1;
    },
    closeModal() {
      this.isModalShown = false;
    },
    getSelectedPrimitives(rowId) {
      const inputsLineData = document.querySelectorAll('#line-data');
      const inputsPolygonsData = document.querySelectorAll('#polygon-data');

      if (this.geometricPrimitives[rowId].length)
        this.geometricPrimitives[rowId] = [];

      inputsLineData.forEach((input) => {
        if (input.checked) {
          this.geometricPrimitives[rowId].push(input.value);
        }
      });
      inputsPolygonsData.forEach((input) => {
        if (input.checked) {
          this.geometricPrimitives[rowId].push(input.value);
        }
      });

      this.closeModal();
    },
  },
};
</script>

<style scoped>
.table-container {
  text-align: left;
}
button {
  margin-top: 1.4rem;
  padding: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 1000px;
  border: 1px solid #2b8a3e;
  background-color: #51cf66;
  transition: all 0.3s ease;
}
button:hover {
  background-color: #40c057;
}
button:active {
  background-color: #37b24d;
}
button i {
  font-size: 1.8rem;
  color: #fff;
}
.tr,
::v-deep(.tr) {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
/* .tr:nth-child(even) {
  background-color: var(--light-blue-bg-color);
}
.tr:nth-child(odd) {
  background-color: var(--very-light-blue-bg-color);
} */
</style>
