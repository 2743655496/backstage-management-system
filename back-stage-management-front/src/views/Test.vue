<template>
  <div class="tab-switcher">
    <div
      v-for="tab in tabs"
      :key="tab.label"
      :class="['tab-item', { active: tab.label === activeTab }]"
      @click="activeTab = tab.label"
    >
      <i :class="tab.icon" class="tab-icon"></i>
      <span class="tab-label">{{ tab.label }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TabSwitcher',
  data() {
    return {
      activeTab: '流量趋势',
      tabs: [
        { label: '流量趋势', icon: 'el-icon-data-board' },
        { label: '月访问量', icon: 'el-icon-date' }
      ]
    };
  }
};
</script>

<style lang="less" scoped>
.tab-switcher {
  display: flex;
  border-radius: 24px;
  overflow: hidden;
  background-color: #ecf0f1;
  width: fit-content;
  .tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  color: #7f8c8d;
  background-color: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-item.active {
  background-color: #ffffff;
  color: #2c3e50;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.tab-icon {
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
}


</style>
