<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
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
        legend: {
          orient: "horizontal",
          bottom: 15, // ✅ 距离底部 20px
          left: "center",
        },

        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            saveAsImage: { show: true },
          },
        },
        series: [
          {
            name: "访问结构",
            type: "pie",
            radius: [30, 100], // ✅ 缩小图形尺寸
            center: ["50%", "50%"], // ✅ 调整位置居中偏下
            roseType: "area",
            itemStyle: {
              borderRadius: 8,
            },
            label: {
              show: true,
              fontSize: 14,
            },
            data: this.chartData,
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
  height: 100%; /* ✅ 不再用 aspect-ratio 或 padding 技巧 */
  overflow: hidden;
}
</style>
