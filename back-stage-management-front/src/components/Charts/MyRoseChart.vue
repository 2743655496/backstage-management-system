<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
import { mapGetters } from "vuex";
import * as echarts from "echarts/core";
import { ToolboxComponent, LegendComponent } from "echarts/components";
import { PieChart } from "echarts/charts";
import { LabelLayout } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  ToolboxComponent,
  LegendComponent,
  PieChart,
  CanvasRenderer,
  LabelLayout,
]);

let resizeTimer = null;

export default {
  name: "RoseChart",
  props: {
    theme: {
      type: String,
      default: "light",
    },
    chartData: {
      type: Array,
      default: () => [
        { value: 40, name: "外包" },
        { value: 38, name: "技术支持" },
        { value: 32, name: "远程" },
        { value: 30, name: "定制" },
      ],
    },
  },

  computed: {
    ...mapGetters("LightModule", ["textColor"]),
  },

  data() {
    return {
      chartInstance: null,
      isMounted: false,
      _resizeHandler: null,
    };
  },

  mounted() {
    this.isMounted = true;
    this.safeInitChart();
  },

  beforeDestroy() {
    this.isMounted = false;
    if (this._resizeHandler) {
      window.removeEventListener("resize", this._resizeHandler);
    }
    if (this.chartInstance) {
      this.chartInstance.dispose();
      this.chartInstance = null;
    }
  },

  watch: {
    // Vuex 文字颜色变化 → 更新图表
    textColor() {
      if (this.chartInstance) {
        this.chartInstance.setOption(this.getChartOption());
      }
    },

    // ECharts 主题变化 → 必须重新 init
    theme() {
      this.reRenderChart();
    },
  },

  methods: {
    safeInitChart() {
      this.$nextTick(() => {
        setTimeout(() => {
          if (!this.isMounted) return;

          const container = this.$refs.chartRef;
          if (!container || container.offsetWidth === 0) return;

          this.chartInstance = echarts.init(container, this.theme);
          this.chartInstance.setOption(this.getChartOption());

          this._resizeHandler = () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
              if (this.chartInstance) {
                this.chartInstance.resize();
              }
            }, 200);
          };

          window.addEventListener("resize", this._resizeHandler);
        }, 300);
      });
    },

    // 主题切换时重新渲染图表
    reRenderChart() {
      const container = this.$refs.chartRef;
      if (!container) return;

      if (this.chartInstance) {
        this.chartInstance.dispose();
      }

      this.chartInstance = echarts.init(container, this.theme);
      this.chartInstance.setOption(this.getChartOption());
    },

    getChartOption() {
      const container = this.$refs.chartRef;
      const width = container ? container.offsetWidth : 300;

      const minRadius = width * 0.1;
      const maxRadius = width * 0.3;

      return {
        tooltip: {
          trigger: "item",
        },

        legend: {
          orient: "horizontal",
          bottom: 15,
          left: "center",
          textStyle: {
            color: this.textColor, // 图例文字颜色
          },
        },

        toolbox: {
          show: true,
          feature: {
            saveAsImage: { show: true },
          },
        },

        series: [
          {
            name: "访问结构",
            type: "pie",
            roseType: "area",
            radius: [minRadius, maxRadius],
            center: ["50%", "50%"],

            itemStyle: {
              borderRadius: 8,
            },

            label: {
              show: true,
              fontSize: 14,
              color: this.textColor, // 标签文字颜色
            },

            data: this.chartData,
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>
