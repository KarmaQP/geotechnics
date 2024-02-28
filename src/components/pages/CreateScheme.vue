<template>
  <section>
    <h1 class="bubble">Этап 1. Создание расчетной схемы</h1>
    <div class="control-btns">
      <a class="bubble" href="https://google.com" target="_blank"
        >Скачать программу gmsh</a
      >
      <a
        class="bubble"
        href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        target="_blank"
        >Инструкция по созданию схемы</a
      >
    </div>
    <div>
      <h2>Выберите тип задачи</h2>
      <select v-model="taskType">
        <option selected value="elasticity-nonlinearity">
          Задача упругости и нелинейности
        </option>
        <option value="filtration">Задача фильтрации</option>
        <option value="temperature">Задача температуры</option>
      </select>
    </div>
    <label for="files" class="drop-container" id="dropcontainer">
      <span class="drop-title">Перенесите файл gmsh</span>
      или
      <input type="file" id="files" required />
    </label>
    <button
      @click="displaySchemeAndTable"
      class="bubble btn"
      :class="disabledButton"
    >
      Загрузить расчетную схему
    </button>
    <div class="line"></div>
    <the-figure figure-name="fig01"></the-figure>
    <!-- <table-materials v-if="gmshData"></table-materials> -->
  </section>
</template>

<script>
// import TableMaterials from '../UI/TableMaterials.vue';
import { mapActions } from 'vuex';
import { mapGetters } from 'vuex';
import axios from 'axios';

import { isProxy, toRaw } from 'vue';

/* global mpld3 */
/* global d3 */
/* global $ */

export default {
  // components: {
  //   TableMaterials,
  // },
  data() {
    return {
      isFileLoaded: false,
      taskType: 'elasticity-nonlinearity',
    };
  },
  computed: {
    ...mapGetters([
      'gmshData',
      'calculatedSchemeData',
      'linesData',
      'polygonsData',
      'coordsData',
      'isLoading',
    ]),
    disabledButton() {
      if (this.isLoading) return 'disabled__btn';
      else return '';
    },
  },
  methods: {
    ...mapActions([
      'sendTaskType',
      'sendDataFromFile',
      'sendLinesData',
      'sendPolygonsData',
      'sendCoordsData',
      'sendPropertiesData',
      'sendCharacteristicsData',
      'sendStageData',
      'sendToast',
      'sendIsLoading',
    ]),
    async displaySchemeAndTable() {
      this.sendLinesData({ linesData: [] });
      this.sendPolygonsData({ polygonsData: [] });
      this.sendCoordsData({ coordsData: [] });
      this.sendPropertiesData({ propertiesData: {} });
      this.sendCharacteristicsData({ characteristicsData: {} });
      this.sendStageData({ stageData: {} });

      const fileInput = document.getElementById('files');

      // checking if everything is ok
      if (!this.isFileLoaded) {
        this.sendToast({
          toastInfo: { msg: 'Необходимо загрузить gmsh файл!', type: 'error' },
        });
        return;
      }
      if (fileInput.files.length > 1) {
        this.sendToast({
          toastInfo: {
            msg: 'Необходимо загрузить лишь один gmsh файл!',
            type: 'error',
          },
        });
        return;
      }
      if (fileInput.files[0].type !== '') {
        this.sendToast({
          toastInfo: {
            msg: 'Необходимо загрузить файл из gmsh!',
            type: 'error',
          },
        });
        return;
      }

      this.sendToast({
        toastInfo: { msg: 'Загрузка файла...', type: 'info' },
      });

      this.sendIsLoading({ isLoading: true });

      // read data from file, sending to store, display scheme+table
      const fr = new FileReader();
      fr.readAsText(fileInput.files[0]);

      fr.onload = async () => {
        const responseData = await this.getData(fileInput.files[0]);
        this.sendTaskType({ taskType: this.taskType });

        console.log(responseData);
        if (responseData.status === 400) {
          // this.$emit('show-notification', responseData.msg, 'error');
          this.sendToast({
            toastInfo: { msg: responseData.msg, type: 'error' },
          });
          this.sendIsLoading({ isLoading: false });
          return;
        }

        // const gmshContentRes = await fetch(responseData.gmsh_file_path);
        // console.log(gmshContentRes);
        // const gmshContentReader = gmshContentRes.body.getReader();
        // console.log(gmshContentReader);

        const jsonData = JSON.parse(responseData.json);
        const calculatedSchemeData = responseData.calculatedSchemeData;

        // TODO: send data from parser to store
        // NOTE: look for getDataFromFile function
        this.sendDataFromFile({
          jsonData: jsonData,
          calculatedSchemeData: calculatedSchemeData,
        });

        // TODO: draw figure
        // NOTE: look for drawFigure function
        this.drawFigure();

        if (!isProxy(this.calculatedSchemeData)) return;

        // parsing the parser ;D and send to store
        const rawCalcSchemeData = toRaw(this.calculatedSchemeData);
        const linesData = rawCalcSchemeData.list_node_line;
        const polygonsData = rawCalcSchemeData.list_node_polygon;
        const coordsData = rawCalcSchemeData.list_node_coor;

        // linesData (store)
        let tempArray = [];
        Object.entries(linesData).forEach((item) => {
          tempArray.push(item);
        });
        this.sendLinesData({ linesData: tempArray });

        // console.log(tempArray);
        // console.log(linesData);

        // polygonsData (store)
        tempArray = [];
        Object.entries(polygonsData).forEach((item) => {
          tempArray.push(item);
        });
        this.sendPolygonsData({ polygonsData: tempArray });

        // console.log(tempArray);
        // console.log(polygonsData);

        // coordsData (store)
        tempArray = [];
        Object.entries(coordsData).forEach((item) => {
          tempArray.push(item);
        });
        this.sendCoordsData({ coordsData: tempArray });

        // console.log(tempArray);
        // console.log(coordsData);

        console.log(this.taskType);

        this.sendToast({ toastInfo: { msg: responseData.msg, type: 'ok' } });

        this.sendIsLoading({
          isLoading: false,
        });
      };
    },
    async getData(gmshFile) {
      const formData = new FormData();
      const csrf = $('input[name=csrfmiddlewaretoken]').val();

      formData.append('gmshFile', gmshFile);
      formData.append('csrfmiddlewaretoken', csrf);
      formData.append('taskType', this.taskType);

      const response = await axios.post('api/parser_data/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    },
    drawFigure() {
      const fig = document.querySelector('#fig01');
      fig.innerHTML = '';
      mpld3.draw_figure('fig01', this.gmshData);

      const legend = document.querySelector('.mpld3-staticpaths');
      Array.from(legend.children).forEach((child, i) => {
        if (i === 0) child.remove();
        if (i > 0) {
          Array.from(child.children).forEach((circle, j) => {
            if (j < 2) circle.remove();
          });
        }
      });
    },
  },
  mounted() {
    const dropContainer = document.getElementById('dropcontainer');
    const fileInput = document.getElementById('files');

    fileInput.addEventListener('change', () => (this.isFileLoaded = true));

    dropContainer.addEventListener(
      'dragover',
      (e) => {
        // prevent default to allow drop
        e.preventDefault();
      },
      false
    );

    dropContainer.addEventListener('dragenter', () => {
      dropContainer.classList.add('drag-active');
    });

    dropContainer.addEventListener('dragleave', () => {
      dropContainer.classList.remove('drag-active');
    });

    dropContainer.addEventListener('drop', (e) => {
      e.preventDefault();
      dropContainer.classList.remove('drag-active');
      fileInput.files = e.dataTransfer.files;
      this.isFileLoaded = true;
    });
  },
};
</script>

<style scoped>
section {
  text-align: center;
}

.control-btns {
  text-align: center;
  max-width: 20rem;
  line-height: 1.4;
  margin-bottom: 3.6rem;

  display: flex;
  flex-direction: column;
  gap: 2.4rem;
}

.btn {
  margin-top: 2.4rem;
  padding: 2rem;
}

h2 {
  font-size: 2rem;
}

select {
  margin: 1.6rem 0 3.2rem 0;
  font-size: 1.6rem;
  border: 1px solid #000;
  border-radius: 8px;
  min-width: 40rem;
}

select,
option {
  font-family: inherit;
}

.bubble {
  font-size: 2rem;
}

.line {
  background-color: var(--blue-bg-color);
  height: 0.6rem;
  margin-top: 3.2rem;
}

.drop-container {
  position: relative;
  display: flex;
  gap: 10px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 200px;
  padding: 20px;
  border-radius: 10px;
  border: 2px dashed #555;
  color: #444;
  cursor: pointer;
  transition: background 0.2s ease-in-out, border 0.2s ease-in-out;
}

.drop-container:hover,
.drop-container.drag-active {
  background: #eee;
  border-color: #111;
}

.drop-container:hover .drop-title,
.drop-container.drag-active .drop-title {
  color: #222;
}

.drop-title {
  color: #444;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  transition: color 0.2s ease-in-out;
}

input[type='file'] {
  width: 350px;
  max-width: 100%;
  color: #444;
  padding: 5px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #555;
}

input[type='file']::file-selector-button {
  margin-right: 20px;
  border: none;
  background: #084cdf;
  padding: 10px 20px;
  border-radius: 10px;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
  font-family: inherit;
}

input[type='file']::file-selector-button:hover {
  background: #0d45a5;
}

input {
  min-height: 0;
  min-width: 0;
}

#fig01 {
  transform: translateX(-38%);
}
</style>
