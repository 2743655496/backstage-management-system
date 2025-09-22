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
      isMounted: false, // ✅ 挂载标志
      _resizeHandler: null,
    };
  },
  mounted() {
    this.isMounted = true;
    this.safeInitChart(); // ✅ 使用封装方法
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
        }, 300); // ✅ 延迟初始化，确保容器尺寸稳定
      });
    },
    getChartOption() {
      return {
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
            "1月", "2月", "3月", "4月", "5月", "6月",
            "7月", "8月", "9月", "10月", "11月", "12月",
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
