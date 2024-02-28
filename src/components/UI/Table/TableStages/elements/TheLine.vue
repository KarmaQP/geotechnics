<template>
  <div class="generated-table">
    <div class="tr">
      <div class="td">{{ newPropertyData[0] }}</div>
      <div class="td">
        <div v-if="newPropertyData[1].loadProperty">
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
              <input
                type="number"
                :id="`input__load--${newPropertyData[0].toLowerCase()}`"
              />
            </div>
          </div>
        </div>
        <div v-if="newPropertyData[1].boundaryCondition">
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
            <div
              class="input-container"
              v-if="taskType === 'elasticity-nonlinearity'"
            >
              <label>ux, м = </label>
              <input
                type="number"
                :id="`input__bound-x--${newPropertyData[0].toLowerCase()}`"
              />
            </div>
            <div
              class="input-container"
              v-if="taskType === 'elasticity-nonlinearity'"
            >
              <label>uy, м = </label>
              <input
                type="number"
                :id="`input__bound-y--${newPropertyData[0].toLowerCase()}`"
              />
            </div>
            <div class="input-container" v-if="taskType === 'filtration'">
              <label>Узловой напор = </label>
              <input
                type="number"
                :id="`input__nodal-pressure--${newPropertyData[0].toLowerCase()}`"
              />
            </div>
            <div class="input-container" v-if="taskType === 'temperature'">
              <label>Температура на границе, °C = </label>
              <input
                type="number"
                :id="`input__temperature--${newPropertyData[0].toLowerCase()}`"
              />
            </div>
            <div class="input-container" v-if="taskType === 'temperature'">
              <label>Начальная температура, °C = </label>
              <input
                type="number"
                :id="`input__initial-temperature--${newPropertyData[0].toLowerCase()}`"
              />
            </div>
          </div>
        </div>
        <div v-if="newPropertyData[1].plateProperty">
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
              <select
                :id="`select__plate--${newPropertyData[0].toLowerCase()}`"
              >
                <option value="null"></option>
                <option
                  v-for="char in plateCharacteristics"
                  :key="Object.entries(char)[0][0]"
                  :value="Object.entries(char)[0][0]"
                >
                  {{ Object.entries(char)[0][0] }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div v-if="newPropertyData[1].spacerProperty">
          <div class="toggle-container">
            <i
              class="fa-solid"
              :class="balkIconState"
              @click="toggleBalkInfo"
            ></i>
            <div>Распорка</div>
          </div>
          <div class="info-container" v-show="showBalkInfo">
            <div class="input-container input-container--select">
              <label>Выбор материала распорки:</label>
              <select
                :id="`select__spacer--${newPropertyData[0].toLowerCase()}`"
              >
                <option value="null"></option>
                <option
                  v-for="char in spacerCharacteristics"
                  :key="Object.entries(char)[0][0]"
                  :value="Object.entries(char)[0][0]"
                >
                  {{ Object.entries(char)[0][0] }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="td">
        <select :id="`select__activity--${newPropertyData[0].toLowerCase()}`">
          <option selected :value="true">Да</option>
          <option :value="false">Нет</option>
        </select>
      </div>

      <div class="td">
        <input
          type="text"
          :id="`input__comment--${newPropertyData[0].toLowerCase()}`"
          placeholder="Введите текст..."
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  props: ['propertyData'],
  computed: {
    ...mapGetters(['taskType', 'propertiesData', 'characteristicsData']),
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
      plateCharacteristics: [],
      spacerCharacteristics: [],
      showLoadInfo: false,
      showBoundCondInfo: false,
      showPlateInfo: false,
      showBalkInfo: false,
      newPropertyData: {},
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
    initProperties() {
      this.characteristicsData.oneDimData.forEach((data) => {
        switch (Object.values(data)[0].workType) {
          case 'stretching-compression':
            this.spacerCharacteristics.push(data);
            break;
          case 'stretching-compression-bending':
            this.plateCharacteristics.push(data);
            break;
        }
      });

      // console.log(this.propertyData);
      this.newPropertyData = Object.entries(this.propertyData)[0];
      // this.newPropertyData = Object.entries(this.propertyData[1])[0];
      // console.log(this.newPropertyData);
    },
  },
  beforeMount() {
    this.characteristicsData.oneDimData?.forEach((data) => {
      console.log(data);
      switch (Object.values(data)[0].workType) {
        case 'stretching-compression':
          this.spacerCharacteristics.push(data);
          break;
        case 'stretching-compression-bending':
          this.plateCharacteristics.push(data);
          break;
      }
    });

    this.newPropertyData = Object.entries(this.propertyData)[0];
  },
  updated() {
    console.log('Updated TheLine');
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
  flex: 2;
}

.input-container input[type='number'] {
  border: 1px solid #000;
  background-color: var(--bg-color);
  min-height: 0;
  min-width: 0;
  flex: 1.5;
}

select,
option {
  font-family: inherit;
}
</style>
