<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
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
        }, 300); // ✅ 延迟初始化，确保容器尺寸稳定
      });
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
            },
            emphasis: {
              label: {
                show: true,
                fontWeight: "bold",
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
