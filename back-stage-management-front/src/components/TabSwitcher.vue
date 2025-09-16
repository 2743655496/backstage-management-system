<template>
  <div class="tab-switcher">
    <div
      v-for="tab in tabs"
      :key="tab.label"
      :class="['tab-item', { active: tab.label === currentTab }]"
      @click="handleClick(tab.label)"
    >
      <i :class="tab.icon" class="tab-icon"></i>
      <span class="tab-label">{{ tab.label }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TabSwitcher',
  props: {
    tabs: Array,
    activeTab: String
  },
  data() {
    return {
      currentTab: this.activeTab
    };
  },
  watch: {
    activeTab(newVal) {
      this.currentTab = newVal;
    }
  },
  methods: {
    handleClick(label) {
      if (label !== this.currentTab) {
        this.currentTab = label;
        this.$emit('update:activeTab', label); // v-model 更新
        this.$emit('tab-change', label);       // 业务逻辑触发
      }
    }
  }
};
</script>

<style scoped>
.tab-switcher {
  display: flex;
  border-radius: 24px;
  overflow: hidden;
  background-color: #ecf0f1;
  width: fit-content;
  margin-bottom: 20px;
}
.tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  color: #7f8c8d;
  background-color: transparent;
  cursor: pointer;
  transition: all 0.1s ease;
}
.tab-item.active {
  background-color: #ffffff;
  color: #2c3e50;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.tab-icon {
  font-size: 18px;
  pointer-events: none;
}
</style>
