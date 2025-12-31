<template>
  <div class="tab-switcher">
    <div
      v-for="tab in tabs"
      :key="tab.label"
      :class="[
        'tab-item',
        { active: tab.label === currentTab },
        { 'with-transition': isClicking }
      ]"
      @click="handleClick(tab.label)"
    >
      <i :class="tab.icon" class="tab-icon"></i>
      <span class="tab-label">{{ tab.label }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "TabSwitcher",
  props: {
    tabs: Array,
    activeTab: String,
    backgroundColor: {
      type: String,
      default: "#ecf0f1",
    },
    activeBackgroundColor: {
      type: String,
      default: "#ffffff",
    },
    textColor: {
      type: String,
      default: "#7f8c8d",
    },
    activeTextColor: {
      type: String,
      default: "#2c3e50",
    },
  },
  data() {
    return {
      currentTab: this.activeTab,
      isClicking: false, // 控制是否启用 transition
    };
  },
  watch: {
    activeTab(newVal) {
      this.currentTab = newVal;
    },
  },
  methods: {
    handleClick(label) {
      if (label !== this.currentTab) {
        // 点击时开启 transition
        this.isClicking = true;

        this.currentTab = label;
        this.$emit("update:activeTab", label);
        this.$emit("tab-change", label);

        // 动画结束后关闭 transition
        setTimeout(() => {
          this.isClicking = false;
        }, 150);
      }
    },
  },
};
</script>

<style lang="less" scoped>
.tab-switcher {
  display: flex;
  border-radius: 24px;
  overflow: hidden;
  background-color: v-bind(backgroundColor);
  width: fit-content;
  margin-bottom: 20px;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  color: v-bind(textColor);
  background-color: transparent;
  cursor: pointer;
}

/* 只有点击时才启用动画 */
.tab-item.with-transition {
  transition: all 0.1s ease;
}

.tab-item.active {
  background-color: v-bind(activeBackgroundColor);
  color: v-bind(activeTextColor);
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.tab-icon {
  font-size: 18px;
  pointer-events: none;
}
</style>
