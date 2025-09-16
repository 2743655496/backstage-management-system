<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script>
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
          data: ["访问", "趋势"],
        },
        radar: {
          indicator: [
            { name: "网页", max: 10000 },
            { name: "其他", max: 10000 },
            { name: "第三方", max: 10000 },
            { name: "客户端", max: 10000 },
            { name: "Ipad", max: 10000 },
            { name: "移动端", max: 10000 },
          ],
        },
        series: [
          {
            name: "访问趋势",
            type: "radar",
            symbol: "circle", // 点位样式
            symbolSize: 6,
            lineStyle: {
              width: 2,
            },
            areaStyle: {
              opacity: 0.3, // 填充透明度
            },
            emphasis: {
              focus: "series",
              lineStyle: {
                width: 4, // 悬停时线条加粗
              },
              areaStyle: {
                opacity: 0.6, // 悬停时填充更密集
              },
            },
            data: [
              {
                value: [4200, 3000, 2000, 3500, 5000, 1800],
                name: "访问",
              },
              {
                value: [5000, 4000, 2800, 2600, 4200, 2100],
                name: "趋势",
              },
            ],
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
