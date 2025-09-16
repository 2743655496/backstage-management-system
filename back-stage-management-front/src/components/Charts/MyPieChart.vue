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
      lastWidth: window.innerWidth,
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
        radar: {
          radius: "60%", // ✅ 图形大小相对容器宽度
          center: ["50%", "50%"], // ✅ 居中显示
        },
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
