<template>
  <section>
    <h1 class="bubble">Этап 5. Результаты расчета</h1>
    <div class="figures__container">
      <div id="fig1__container">
        <the-figure figure-name="fig1"></the-figure>
        <div id="min-max-values-fig1" class="min-max-values__container"></div>
      </div>
      <div id="fig2__container">
        <div class="solver-step__container"></div>
        <the-figure figure-name="fig2"></the-figure>
        <div id="min-max-values-fig2" class="min-max-values__container"></div>
      </div>
      <div id="fig3__container">
        <the-figure figure-name="fig3"></the-figure>
        <div id="min-max-values-fig3" class="min-max-values__container"></div>
      </div>
      <div id="fig4__container">
        <the-figure figure-name="fig4"></the-figure>
        <div id="min-max-values-fig4" class="min-max-values__container"></div>
      </div>
      <div id="fig5__container">
        <the-figure figure-name="fig5"></the-figure>
        <div id="min-max-values-fig5" class="min-max-values__container"></div>
      </div>
      <div id="fig6__container">
        <the-figure figure-name="fig6"></the-figure>
        <div id="min-max-values-fig6" class="min-max-values__container"></div>
      </div>
      <div id="fig7__container">
        <the-figure figure-name="fig7"></the-figure>
        <div id="min-max-values-fig7" class="min-max-values__container"></div>
      </div>
      <div id="fig8__container">
        <the-figure figure-name="fig8"></the-figure>
        <div id="min-max-values-fig8" class="min-max-values__container"></div>
      </div>
      <div id="fig9__container">
        <the-figure figure-name="fig9"></the-figure>
        <div id="min-max-values-fig9" class="min-max-values__container"></div>
      </div>
      <div id="fig10__container">
        <the-figure figure-name="fig10"></the-figure>
        <div id="min-max-values-fig10" class="min-max-values__container"></div>
      </div>
      <div id="fig11__container">
        <the-figure figure-name="fig11"></the-figure>
        <div id="min-max-values-fig11" class="min-max-values__container"></div>
      </div>
      <div id="fig12__container">
        <the-figure figure-name="fig12"></the-figure>
        <div id="min-max-values-fig12" class="min-max-values__container"></div>
      </div>
      <div id="fig13__container">
        <the-figure figure-name="fig13"></the-figure>
        <div id="min-max-values-fig13" class="min-max-values__container"></div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import axios from 'axios';

/* global mpld3 */
/* global $ */
/* global d3 */

export default {
  computed: {
    ...mapGetters([
      'taskType',
      'stageData',
      'coordsData',
      'polygonsData',
      'linesData',
      'isUpdated',
    ]),
  },
  data() {
    return {
      values: {},
      stepNum: 0,
    };
  },
  async beforeMount() {
    // var scripts = document.getElementsByTagName('script'),
    //   src = scripts[scripts.length - 1].src;
    this.sendToast({
      toastInfo: { msg: 'Загрузка расчетов...', type: 'info' },
    });

    this.sendIsLoading({ isLoading: true });

    console.log(this.taskType);
    const responseData = await this.loadSolverData(this.taskType);

    this.sendIsLoading({ isLoading: false });
  },
  async mounted() {
    this.initToolTip();
  },
  async updated() {
    console.log(`isUpdated: ${this.isUpdated}`);
    if (!this.isUpdated) return;

    this.sendToast({
      toastInfo: { msg: 'Обновление результатов...', type: 'info' },
    });

    this.sendIsLoading({ isLoading: true });

    console.log('Updated CalculatedResults');

    // Reset mpld3 tool tips and figs
    const mpld3Tooltips = document.querySelectorAll('.mpld3-tooltip');

    mpld3Tooltips.forEach((tooltip) => tooltip.remove());

    for (let i = 0; i < 13; i++) {
      const fig = document.querySelector(`#fig${i + 1}`);
      fig.innerHTML = '';
    }

    // Reset ui input and button
    const inputSteps = document.querySelector('#step-num');
    const btnSteps = document.querySelector('#solver-btn');

    if (inputSteps) {
      inputSteps.remove();
      btnSteps.remove();
    }

    // Reset min max values container
    const minMaxValues = document.querySelectorAll(
      '.min-max-values__container'
    );

    minMaxValues.forEach((minMaxContainer) => {
      minMaxContainer.innerHTML = '';
    });

    // Load new data and figs
    const responseData = await this.loadSolverData(this.taskType);

    this.initToolTip();

    this.sendIsLoading({ isLoading: false });
  },
  methods: {
    ...mapActions(['sendToast', 'sendIsUpdated', 'sendIsLoading']),
    async loadSolverData(taskType) {
      if (this.isUpdated) {
        this.stepNum = 0;
      }

      const csrf = $('input[name=csrfmiddlewaretoken]').val();
      const response = await axios.post(
        'api/solver/',
        {
          task_type: taskType,
          input_data: this.stageData,
          coor_data: this.coordsData,
          polygons_data: this.polygonsData,
          lines_data: this.linesData,
          step_num: this.stepNum,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
          },
        }
      );

      console.log(response.data);
      if (response.data.status === 400) {
        this.sendToast({
          toastInfo: { msg: response.data.msg, type: 'error' },
        });
        return;
      }

      this.values = response.data.min_max_values;
      const minMaxValues = Object.values(this.values);

      if (taskType === 'elasticity-nonlinearity') {
        this.sendToast({
          toastInfo: { msg: 'Расчет упругости успешно завершен!', type: 'ok' },
        });

        for (let i = 1; i <= 13; i++) {
          const path = `static/src/dist/results/isofields_${i}.json`;
          const res = await fetch(path);
          const json = await res.json();

          const fig = document.querySelector(`#fig${i}`);
          const valuesContainer = document.querySelector(
            `#min-max-values-fig${i}`
          );

          fig.innerHTML = '';

          valuesContainer.innerHTML = `
            <div class="min-max-values__container">
              <div class="fig-max" style="margin-bottom: 0.6rem;">
                Макс. значение: ${minMaxValues[i - 1].max}
              </div>
              <div class="fig-min">
                Мин. значение: ${minMaxValues[i - 1].min}
              </div>
            </div>
          `;

          mpld3.draw_figure(`fig${i}`, json);
        }
      } else if (taskType === 'filtration') {
        this.sendToast({
          toastInfo: { msg: 'Расчет фильтрации успешно завершен!', type: 'ok' },
        });

        for (let i = 1; i <= 9; i++) {
          const path = `static/src/dist/results/filtration/isofields_${i}.json`;
          const res = await fetch(path);
          const json = await res.json();

          const fig = document.querySelector(`#fig${i}`);
          const valuesContainer = document.querySelector(
            `#min-max-values-fig${i}`
          );

          fig.innerHTML = '';

          if (i <= 8) {
            valuesContainer.innerHTML = `
              <div class="min-max-values__container">
                <div class="fig-max" style="margin-bottom: 0.6rem;">
                  Макс. значение: ${minMaxValues[i - 1].max}
                </div>
                <div class="fig-min">
                  Мин. значение: ${minMaxValues[i - 1].min}
                </div>
              </div>
            `;
          }

          mpld3.draw_figure(`fig${i}`, json);
        }
      } else if (taskType === 'temperature') {
        const path = `static/src/dist/results/temperature/isofields.json`;
        const res = await fetch(path);
        const json = await res.json();

        const fig = document.querySelector(`#fig2`);
        const valuesContainer = document.querySelector(`#min-max-values-fig2`);
        const solverStepContainer = document.querySelector(
          `.solver-step__container`
        );

        fig.innerHTML = '';

        valuesContainer.innerHTML = `
            <div class="min-max-values__container">
              <div class="fig-max" style="margin-bottom: 0.6rem;">
                Макс. значение: ${minMaxValues[0].max}
              </div>
              <div class="fig-min">
                Мин. значение: ${minMaxValues[0].min}
              </div>
            </div>
          `;

        mpld3.draw_figure(`fig2`, json);

        solverStepContainer.innerHTML = '';
        solverStepContainer.insertAdjacentHTML(
          'afterbegin',
          `
            <select id="step-num"></select>
            <button class="btn bubble" id="solver-btn" @click="test" type="button">Применить</button>
          `
        );

        const selectValues = response.data.select_values;
        const selectContainer = document.querySelector('#step-num');

        selectValues.forEach((value, i) => {
          selectContainer.insertAdjacentHTML(
            'beforeend',
            `
              <option value="${i}">${value}</option>
            `
          );
        });

        // NOTE: maybe bug if steps num > prev. value of steps
        selectContainer.value = this.stepNum;

        const solverBtn = document.querySelector('#solver-btn');
        const that = this;

        solverBtn.addEventListener('click', async function () {
          that.sendToast({
            toastInfo: {
              msg: 'Загрузка новых расчетов...',
              type: 'info',
            },
          });

          that.stepNum = selectContainer.value;
          const responseData = await that.loadSolverData(that.taskType);
          that.initToolTip();
        });

        this.sendToast({
          toastInfo: {
            msg: 'Расчет температуры успешно завершен!',
            type: 'ok',
          },
        });
      }

      this.sendIsUpdated({ isUpdated: false });
    },
    initToolTip() {
      mpld3.register_plugin('htmltooltip', HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ['id'];
      HtmlTooltipPlugin.prototype.defaultProps = {
        labels: null,
        target: null,
        hoffset: 0,
        voffset: 10,
        targets: null,
      };

      function HtmlTooltipPlugin(fig, props) {
        mpld3.Plugin.call(this, fig, props);
      }

      HtmlTooltipPlugin.prototype.draw = function () {
        var obj = mpld3.get_element(this.props.id);
        var labels = this.props.labels;
        var targets = this.props.targets;

        var tooltip = d3
          .select('body')
          .select('div')
          .append('div')
          .attr('class', 'mpld3-tooltip')
          .style('position', 'absolute')
          .style('z-index', '10')
          .style('visibility', 'hidden');

        obj
          .elements()
          .on('mouseover', function (d, i) {
            tooltip.html(labels[i]).style('visibility', 'visible');
          })
          .on(
            'mousemove',
            function (d, i) {
              tooltip
                .style('top', d3.event.pageY + this.props.voffset + 'px')
                .style('left', d3.event.pageX + this.props.hoffset + 'px');
            }.bind(this)
          )
          .on('mouseout', function (d, i) {
            tooltip.style('visibility', 'hidden');
          });
      };
    },
  },
};
</script>

<style scoped>
section {
  max-width: 100%;
}

.figures__container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  text-align: center;
}

select,
option {
  font-family: inherit;
}
</style>
