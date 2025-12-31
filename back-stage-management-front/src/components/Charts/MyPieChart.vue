<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
import { mapGetters } from "vuex";
import * as echarts from "echarts/core";
import { TooltipComponent, LegendComponent } from "echarts/components";
import { PieChart } from "echarts/charts";
import { LabelLayout } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  TooltipComponent,
  LegendComponent,
  PieChart,
  CanvasRenderer,
  LabelLayout,
]);

let resizeTimer = null;

export default {
  name: "PieChart",
  props: {
    theme: {
      type: String,
      default: "light",
    },
    chartData: {
      type: Array,
      default: () => [
        { value: 1048, name: "搜索引擎" },
        { value: 735, name: "直接访问" },
        { value: 580, name: "邮件营销" },
        { value: 484, name: "联盟广告" },
        { value: 300, name: "视频广告" },
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
      return {
        tooltip: {
          trigger: "item",
        },

        toolbox: {
          show: true,
          feature: {
            saveAsImage: { show: true },
          },
        },

        legend: {
          top: "bottom",
          left: "center",
          textStyle: {
            color: this.textColor, // 图例文字颜色
          },
        },

        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,

            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },

            label: {
              show: false,
              position: "center",
              color: this.textColor, // 饼图 label 颜色
            },

            emphasis: {
              label: {
                show: true,
                fontWeight: "bold",
                color: this.textColor, // 高亮时文字颜色
              },
            },

            labelLine: {
              show: false,
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
