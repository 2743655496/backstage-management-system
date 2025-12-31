<template>
  <div class="grid-container">
    <!-- 第一行：数据指标卡片（优化版） -->
    <div class="grid-row row-4">
      <div class="metric-card" v-for="item in metrics" :key="item.label">
        <div class="card-icon" :style="{ backgroundColor: item.color }">
          <i :class="item.icon" class="card-icon-i"></i>
        </div>
        <div class="card-content">
          <div class="card-title">{{ item.label }}</div>
          <div class="card-value">{{ item.value }}</div>
          <div class="card-subtitle">
            {{ item.totalLabel }}：{{ item.total }}
          </div>
        </div>
      </div>
    </div>

    <!-- 第二行：趋势图区域 -->
    <div class="grid-row row-1">
      <div class="grid-box">
        <div>
          <TabSwitcher
            :tabs="tabs"
            :activeTab="activeTab"
            @update:activeTab="activeTab = $event"
            @tab-change="handleTabChange"
            :backgroundColor="tabSwitcherBgColor"
            :activeTextColor="tabSwitcherActiveTextColor"
            :textColor="tabSwitcherTextColor"
            :activeBackgroundColor="tabSwitcherActiveBgColor"
          />
        </div>

        <div class="chart-placeholder">
          <LineChart
            :key="chartRenderKey"
            theme="light"
            v-if="activeTab == '流量趋势'"
          />
          <BarChart :key="chartRenderKey" theme="light" v-else />
        </div>
      </div>
    </div>

    <!-- 第三行：用户行为模块 -->
    <div class="grid-row row-3">
      <div class="grid-box">
        <div>访问数量</div>
        <div class="chart-placeholder">
          <RadarChart :key="chartRenderKey" theme="light" />
        </div>
      </div>
      <div class="grid-box">
        <div>访问来源</div>
        <div class="chart-placeholder">
          <PieChart :key="chartRenderKey" :chartData="pieData" theme="light" />
        </div>
      </div>
      <div class="grid-box">
        <div>访问来源</div>
        <div class="chart-placeholder">
          <RoseChart :key="chartRenderKey" theme="light" />
        </div>
      </div>
    </div>

    <!-- 第四行：结论与建议 -->
    <!-- <div class="grid-row row-2">
      <div class="grid-box">结论总结</div>
      <div class="grid-box">优化建议</div>
    </div> -->
  </div>
</template>

<script>
import LineChart from "@/components/Charts/MyLineChart.vue";
import TabSwitcher from "@/components/TabSwitcher.vue";
import BarChart from "@/components/Charts/MyBarChart.vue";
import RadarChart from "@/components/Charts/MyRadarChart.vue";
import PieChart from "@/components/Charts/MyPieChart.vue";
import RoseChart from "@/components/Charts/MyRoseChart.vue";
import { mapState, mapGetters } from "vuex";
export default {
  name: "AnalysisDashboard",
  components: {
    LineChart,
    TabSwitcher,
    BarChart,
    RadarChart,
    PieChart,
    RoseChart,
  },
  computed: {
    ...mapState("chartRenderKey", ["chartRenderKey"]),
    ...mapGetters("LightModule", [
      "subBackgroundColor",
      "textColor",
      "cardTitleColor",
      "cardValueColor",
      "cardSubtitleColor",
      "tabSwitcherBgColor",
      "tabSwitcherTextColor",
      "tabSwitcherActiveTextColor",
      "tabSwitcherActiveBgColor",
    ]),
  },
  data() {
    return {
      activeTab: "流量趋势",
      tabs: [
        { label: "流量趋势", icon: "el-icon-data-board" },
        { label: "月访问量", icon: "el-icon-date" },
      ],
      metrics: [
        {
          label: "销售额",
          value: "¥1,250,000",
          totalLabel: "总销售额",
          total: "¥8,000,000",
          color: "#3498db",
          icon: "el-icon-goods",
        },
        {
          label: "新增用户",
          value: "8,420",
          totalLabel: "总用户数",
          total: "120,000",
          color: "#2ecc71",
          icon: "el-icon-user",
        },
        {
          label: "访问量",
          value: "20000",
          totalLabel: "总访问量",
          total: "500,000",
          color: "#f39c12",
          icon: "el-icon-thumb",
        },
        {
          label: "使用量",
          value: "5000",
          totalLabel: "总使用量",
          total: "50,000",
          color: "#e74c3c",
          icon: "el-icon-time",
        },
      ],
      pieData: [
        { value: 1048, name: "搜索引擎" },
        { value: 735, name: "直接访问" },
        { value: 580, name: "邮件营销" },
        { value: 484, name: "联盟广告" },
        { value: 300, name: "视频广告" },
      ],
    };
  },
  methods: {
    handleTabChange(label) {
      console.log("切换到标签：", label);
    },
  },
};
</script>

<style lang="less" scoped>
.grid-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: "Helvetica Neue", sans-serif;
  overflow: hidden;
}

/* 每一行使用 grid 布局 */
.grid-row {
  display: grid;
  gap: 20px;
}
.row-4 {
  grid-template-columns: repeat(4, 1fr);
}
.row-3 {
  grid-template-columns: repeat(3, 1fr);
}
.row-2 {
  grid-template-columns: repeat(2, 1fr);
}
.row-1 {
  grid-template-columns: 1fr;
}

/* 格子样式 */
.grid-box {
  background: v-bind(subBackgroundColor);
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  flex-direction: column;
  font-weight: bold;
  color: v-bind(textColor);
  padding: 20px;

  min-width: 0; // ✅ 防止内容撑开 grid 单元格
}

/* 高度控制 */
.row-1 .grid-box,
.row-2 .grid-box,
.row-3 .grid-box {
  height: 393.6px;
}

/* 指标样式 */
/* 第一行卡片样式（替代 grid-box） */
.metric-card {
  background: v-bind(subBackgroundColor);
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 20px;
  transition: transform 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
}

/* 左侧图标块 */
.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  margin-right: 16px;
  display: flex; // 添加 flex 布局
  align-items: center; // 垂直居中
  justify-content: center; // 水平居中
  .card-icon-i {
    font-size: 24px; // 放大图标
    color: #fff; // 图标颜色为白色，增强对比
  }
}

/* 右侧内容区域 */
.card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-title {
  font-size: 16px;
  color: v-bind(cardTitleColor);
}

.card-value {
  font-size: 28px;
  font-weight: bold;
  color: v-bind(cardValueColor);
  margin: 6px 0;
}

.card-subtitle {
  font-size: 14px;
  color: v-bind(cardSubtitleColor);
}

/* 图表占位符 */
.chart-placeholder {
  margin-top: 20px;
  width: 100%;
  height: 90%;
  border-radius: 6px;
  color: #95a5a6;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 响应式处理 */
@media (max-width: 776px) {
  .row-4,
  .row-3,
  .row-2,
  .row-1 {
    grid-template-columns: 1fr;
  }
}

/* 中屏：768px 到 1024px，保持4列 */
@media (min-width: 776px) and (max-width: 1080px) {
  .row-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
