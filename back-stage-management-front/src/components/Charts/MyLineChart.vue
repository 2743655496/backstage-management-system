<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
import { mapGetters } from "vuex";
import * as echarts from "echarts/core";
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from "echarts/components";
import { LineChart } from "echarts/charts";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition,
]);

let resizeTimer = null;

export default {
  name: "LineChart",
  props: {
    theme: {
      type: String,
      default: "light",
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
    // 主题颜色变化 → 重新 setOption
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
      return {
        grid: {
          left: "0px",
          right: "0px",
          top: "60px",
          bottom: "60px",
        },

        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },

        legend: {
          data: ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
          textStyle: { color: this.textColor },
        },

        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },

        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            axisLabel: { color: this.textColor },
            data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          },
        ],

        yAxis: [
          {
            type: "value",
            axisLabel: { color: this.textColor },
          },
        ],

        series: [
          {
            name: "Email",
            type: "line",
            stack: "Total",
            areaStyle: {},
            emphasis: { focus: "series" },
            data: [120, 132, 101, 134, 90, 230, 210],
          },
          {
            name: "Union Ads",
            type: "line",
            stack: "Total",
            areaStyle: {},
            emphasis: { focus: "series" },
            data: [220, 182, 191, 234, 290, 330, 310],
          },
          {
            name: "Video Ads",
            type: "line",
            stack: "Total",
            areaStyle: {},
            emphasis: { focus: "series" },
            data: [150, 232, 201, 154, 190, 330, 410],
          },
          {
            name: "Direct",
            type: "line",
            stack: "Total",
            areaStyle: {},
            emphasis: { focus: "series" },
            data: [320, 332, 301, 334, 390, 330, 320],
          },
          {
            name: "Search Engine",
            type: "line",
            stack: "Total",
            label: {
              show: true,
              position: "top",
              color: this.textColor,
            },
            areaStyle: {},
            emphasis: { focus: "series" },
            data: [820, 932, 901, 934, 1290, 1330, 1320],
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
