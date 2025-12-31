<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
import { mapGetters } from "vuex";
import * as echarts from "echarts/core";
import { TitleComponent, LegendComponent } from "echarts/components";
import { RadarChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([TitleComponent, LegendComponent, RadarChart, CanvasRenderer]);

let resizeTimer = null;

export default {
  name: "RadarChart",
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
        tooltip: {
          trigger: "item",
        },

        legend: {
          data: ["访问", "趋势"],
          textStyle: {
            color: this.textColor, // 图例文字颜色
          },
        },

        radar: {
          radius: "60%",
          center: ["50%", "50%"],
          indicator: [
            { name: "网页", max: 10000 },
            { name: "其他", max: 10000 },
            { name: "第三方", max: 10000 },
            { name: "客户端", max: 10000 },
            { name: "Ipad", max: 10000 },
            { name: "移动端", max: 10000 },
          ],
          axisName: {
            color: this.textColor, // 雷达图指示器文字颜色
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
            name: "访问趋势",
            type: "radar",
            symbol: "circle",
            symbolSize: 6,

            lineStyle: {
              width: 2,
            },

            areaStyle: {
              opacity: 0.3,
            },

            emphasis: {
              focus: "series",
              lineStyle: {
                width: 4,
              },
              areaStyle: {
                opacity: 0.6,
              },
            },

            data: [
              {
                value: [4200, 3000, 2000, 3500, 5000, 1800],
                name: "访问",
                label: {
                  color: this.textColor, // 数据点文字颜色
                },
              },
              {
                value: [5000, 4000, 2800, 2600, 4200, 2100],
                name: "趋势",
                label: {
                  color: this.textColor,
                },
              },
            ],
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
