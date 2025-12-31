<template>
  <div class="workbench-container">
    <div class="workbench-scroll">
      
      <!-- 第一块：沾满宽度 -->
      <div class="grid-row row-1">
        <div class="grid-box full-box">
          <h2 class="welcome-title">欢迎回来，管理员！</h2>
          <p class="welcome-subtitle">这里是您的工作台概览。</p>
        </div>
      </div>

      <!-- 第二块：左右两大块 -->
      <div class="grid-row row-2">
        
        <!-- 左侧大块（2块） -->
        <div class="left-column">
          <div class="grid-box">
            <h3>项目</h3>
            <div class="content-placeholder">项目内容区域</div>
          </div>

          <div class="grid-box">
            <h3>最新动态</h3>
            <div class="content-placeholder">最新动态内容区域</div>
          </div>
        </div>

        <!-- 右侧大块（3块） -->
        <div class="right-column">
          <div class="grid-box">
            <h3>快捷导航</h3>
            <div class="content-placeholder">快捷导航内容区域</div>
          </div>

          <div class="grid-box">
            <h3>代办事项</h3>
            <div class="content-placeholder">代办事项内容区域</div>
          </div>

          <div class="grid-box">
            <h3>访问来源</h3>
            <div class="content-placeholder">访问来源内容区域</div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Workbench",
  computed: {
    ...mapGetters("LightModule", ["subBackgroundColor", "textColor"]),
  },
};
</script>

<style lang="less" scoped>

/* 整个页面高度 = 100vh */
.workbench-container {
  height: calc(100vh - 60px); /* 假设顶部导航是 60px */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 内部滚动区域 */
.workbench-scroll {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 第一块 */
.row-1 {
  display: grid;
  grid-template-columns: 1fr;
}

.full-box {
  height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 第二块：高度自动填满剩余空间 */
.row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  flex: 1; /* ⭐ 自动填满剩余空间 */
  gap: 20px;
}

/* 左列 */
.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 左列比例分配 */
.left-column .grid-box:first-child {
  flex: 4; /* 40% */
}
.left-column .grid-box:last-child {
  flex: 6; /* 60% */
}

/* 右列 */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 右列平均分 */
.right-column .grid-box {
  flex: 1;
}

/* 通用卡片 */
.grid-box {
  background: v-bind(subBackgroundColor);
  color: v-bind(textColor);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

/* 内容区域自动填满 */
.content-placeholder {
  flex: 1;
  margin-top: 10px;
  background: rgba(0,0,0,0.05);
  border-radius: 6px;
}

/* 响应式 */
@media (max-width: 900px) {
  .row-2 {
    grid-template-columns: 1fr;
  }
}
</style>
