<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ lineName }}</div>
      <div class="td">
        <select>
          <option value="yes">Да</option>
          <option value="no">Нет</option>
        </select>
      </div>
      <div class="td">
        <div class="toggle-container">
          <i
            class="fa-solid"
            :class="loadIconState"
            @click="toggleLoadInfo"
          ></i>
          <div>Нагрузка</div>
        </div>
        <div class="info-container" v-show="showLoadInfo">
          <div class="input-container">
            <label>q, кПа = </label>
            <input type="number" />
          </div>
        </div>
        <div class="toggle-container">
          <i
            class="fa-solid"
            :class="boundCondIconState"
            @click="toggleBoundCondInfo"
          ></i>
          <div>Граничные условия</div>
        </div>
        <div
          class="info-container info-container--multi"
          v-show="showBoundCondInfo"
        >
          <div class="input-container">
            <label>ux, м = </label>
            <input type="number" />
          </div>
          <div class="input-container">
            <label>uy, м = </label>
            <input type="number" />
          </div>
        </div>
        <div class="toggle-container">
          <i
            class="fa-solid"
            :class="plateIconState"
            @click="togglePlateInfo"
          ></i>
          <div>Плита</div>
        </div>
        <div class="info-container" v-show="showPlateInfo">
          <div class="input-container input-container--select">
            <label>Выбор материала плиты:</label>
            <select>
              <option value="null"></option>
              <option
                v-for="name in characteristicsNames"
                :key="name"
                value="name"
              >
                {{ name }}
              </option>
            </select>
          </div>
        </div>
        <div class="toggle-container">
          <i
            class="fa-solid"
            :class="balkIconState"
            @click="toggleBalkInfo"
          ></i>
          <div>Балка</div>
        </div>
        <div class="info-container" v-show="showBalkInfo">
          <div class="input-container input-container--select">
            <label>Выбор материала балки:</label>
            <select>
              <option value="null"></option>
              <option
                v-for="name in characteristicsNames"
                :key="name"
                value="name"
              >
                {{ name }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <div class="td">
        <input type="text" name="" id="" placeholder="Введите текст..." />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['lineName', 'oneDimData'],
  computed: {
    loadIconState() {
      if (this.showLoadInfo) return 'fa-minus';
      else return 'fa-plus';
    },
    boundCondIconState() {
      if (this.showBoundCondInfo) return 'fa-minus';
      else return 'fa-plus';
    },
    plateIconState() {
      if (this.showPlateInfo) return 'fa-minus';
      else return 'fa-plus';
    },
    balkIconState() {
      if (this.showBalkInfo) return 'fa-minus';
      else return 'fa-plus';
    },
  },
  data() {
    return {
      characteristicsNames: [],
      showLoadInfo: false,
      showBoundCondInfo: false,
      showPlateInfo: false,
      showBalkInfo: false,
    };
  },

  methods: {
    toggleLoadInfo() {
      this.showLoadInfo = !this.showLoadInfo;
    },
    toggleBoundCondInfo() {
      this.showBoundCondInfo = !this.showBoundCondInfo;
    },
    togglePlateInfo() {
      this.showPlateInfo = !this.showPlateInfo;
    },
    toggleBalkInfo() {
      this.showBalkInfo = !this.showBalkInfo;
    },
  },
  beforeMount() {
    this.oneDimData.forEach((data) => {
      this.characteristicsNames.push(Object.entries(data)[0][0]);
    });
  },
};
</script>

<style scoped>
.toggle-container {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.toggle-container i {
  color: #000;
  border-radius: 1000px;
  border: 1px solid #000;
  background-color: #51cf66;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.toggle-container i::before {
  width: 1.4rem;
  height: 1.4rem;
  /* transform: translateX(1px); */
  transform: translate(0.8px, 0.5px);
}

.info-container {
  margin-bottom: 0.8rem;
}

.input-container {
  display: flex;
}

.input-container--select {
  flex-direction: column;
}

.input-container--select select {
  border: 2px solid #000;
  background-color: var(--blue-bg-color);
  color: #fff;
  border-radius: 8px;
  padding: 0.2rem 0;
}

/* TODO: Переделать последний чайлд, чтоб не было отступа! */
.info-container:nth-last-child() {
  margin-bottom: 0;
}

.info-container--multi {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.input-container label {
  flex: 1;
}

.input-container input[type='number'] {
  border: 1px solid #000;
  background-color: var(--bg-color);
  min-height: 0;
  min-width: 0;
  flex: 2;
}
</style>
