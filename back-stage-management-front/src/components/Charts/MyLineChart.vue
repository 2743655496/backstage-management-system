<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
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
  data() {
    return {
      chartInstance: null,
      isMounted: false, // ✅ 挂载标志
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
    }, 300); // ✅ 延迟 300ms 等待容器宽度稳定
  });
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
            data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          },
        ],
        yAxis: [
          {
            type: "value",
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
