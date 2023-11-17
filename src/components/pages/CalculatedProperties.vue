<template>
  <section>
    <the-isofields></the-isofields>
    <table-properties></table-properties>
  </section>
</template>

<script>
import TableProperties from '../UI/TableProperties.vue';

/* global mpld3 */
/* global d3 */

export default {
  props: ['isCalculated', 'dataJSON'],
  emits: ['toggle-is-calculated'],
  components: {
    TableProperties,
  },
  data() {
    return {};
  },
  methods: {
    mpld3_load_lib(url, callback) {
      var s = document.createElement('script');
      s.src = url;
      s.async = true;
      s.onreadystatechange = s.onload = callback;
      s.onerror = function () {
        console.warn('failed to load library ' + url);
      };
      document.getElementsByTagName('head')[0].appendChild(s);
    },
  },
  mounted() {
    const that = this;
    this.mpld3_load_lib('https://d3js.org/d3.v5.js', function () {
      that.mpld3_load_lib(
        'https://mpld3.github.io/js/mpld3.v0.5.9.js',
        function () {
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
              .select('main')
              .select('#fig01')
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

          mpld3.draw_figure('fig01', that.dataJSON);
        }
      );
    });
  },
};
</script>

<style scoped>
#fig01 {
  margin-left: 5rem;
}
</style>
