<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
import * as echarts from "echarts/core";
import { GridComponent } from "echarts/components";
import { BarChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([GridComponent, BarChart, CanvasRenderer]);
let resizeTimer = null;
export default {
  name: "BarChart",
  props: {
    theme: {
      type: String,
      default: "light",
    },
  },
  data() {
    return {
      chartInstance: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      setTimeout(() => {
        this.initChart();
        window.addEventListener("resize", () => {
          clearTimeout(resizeTimer);
          resizeTimer = setTimeout(() => {
            this.chartInstance.resize();
          }, 200); // ✅ 200ms后执行，用户停止拖动才触发
        });
      }, 300);
    });
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.resizeChart);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  },
  methods: {
    initChart() {
      this.chartInstance = echarts.init(this.$refs.chartRef, this.theme);
      const option = {
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        grid: {
          left: "20px",
          right: "20px",
          top: "40px",
          bottom: "40px",
        },
        xAxis: {
          type: "category",
          data: [
            "1月",
            "2月",
            "3月",
            "4月",
            "5月",
            "6月",
            "7月",
            "8月",
            "9月",
            "10月",
            "11月",
            "12月",
          ],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: [120, 200, 150, 80, 70, 110, 130, 160, 180, 140, 100, 90],
            type: "bar",
          },
        ],
      };
      this.chartInstance.setOption(option);
    },
    resizeChart() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
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
