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

          this.initChart(container);

          this._resizeHandler = () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
              this.resizeChart();
            }, 200);
          };
          window.addEventListener("resize", this._resizeHandler);
        }, 300); // ✅ 延迟初始化，确保容器尺寸稳定
      });
    },
    initChart(container) {
      const containerWidth = container.offsetWidth;
      const minRadius = containerWidth * 0.1;
      const maxRadius = containerWidth * 0.3;

      this.chartInstance = echarts.init(container, this.theme);
      const option = {
        legend: {
          orient: "horizontal",
          bottom: 15,
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
            radius: [minRadius, maxRadius],
            center: ["50%", "50%"],
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
        const container = this.$refs.chartRef;
        if (!container || container.offsetWidth === 0) return;

        const containerWidth = container.offsetWidth;
        const minRadius = containerWidth * 0.1;
        const maxRadius = containerWidth * 0.35;

        this.chartInstance.setOption({
          series: [
            {
              radius: [minRadius, maxRadius],
            },
          ],
        });

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
