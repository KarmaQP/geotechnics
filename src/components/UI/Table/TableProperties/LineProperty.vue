<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td td--header">
        <div class="line-row" @click="toggleInfo">{{ lineName }}</div>
        <div>
          <i class="fa-solid" :class="arrowState" @click="toggleInfo"></i>
        </div>
      </div>

      <div class="td" v-show="infoShow">
        <div class="tr">
          <div class="td">- Свойство плита</div>
          <div class="td td--checkbox-container">
            <input type="checkbox" id="plate-property" name="plate-property" />
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойство нагрузка</div>
          <div class="td td--checkbox-container">
            <input type="checkbox" id="load-property" name="load-property" />
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойство распорка</div>
          <div class="td td--checkbox-container">
            <input
              type="checkbox"
              id="spacer-property"
              name="spacer-property"
            />
          </div>
        </div>
        <div class="tr">
          <div class="td">- Свойства граничное условие</div>
          <div class="td td--checkbox-container">
            <input
              type="checkbox"
              id="boundary-condition-property"
              name="boundary-condition-property"
            />
          </div>
          <!-- <div class="td">
                <select>
                  <option value="yes">Да</option>
                  <option value="no" selected>Нет</option>
                </select>
              </div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'lineName',
    // 'plateProperty',
    // 'loadProperty',
    // 'spacerProperty',
    // 'boundaryConditionProperty',
  ],
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
</style>
