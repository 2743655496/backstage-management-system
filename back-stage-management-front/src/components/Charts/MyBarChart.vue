<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
import { mapGetters } from "vuex";
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
          axisLabel: {
            color: this.textColor, // ← 坐标轴文字颜色
          },
          data: [
            "1月", "2月", "3月", "4月", "5月", "6月",
            "7月", "8月", "9月", "10月", "11月", "12月",
          ],
        },
        yAxis: {
          type: "value",
          axisLabel: {
            color: this.textColor, // ← 坐标轴文字颜色
          },
        },
        series: [
          {
            data: [120, 200, 150, 80, 70, 110, 130, 160, 180, 140, 100, 90],
            type: "bar",
            label: {
              show: true,
              position: "top",
              color: this.textColor, // ← 柱状图顶部文字颜色
            },
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
