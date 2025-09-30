<template>
  <el-submenu v-if="item.children && item.children.length" :index="item.path">
    <template slot="title">
      <i :class="item.icon" v-if="item.icon" class="menu-icon"></i>
      <span>{{ item.name }}</span>
    </template>
    <menu-item
      v-for="child in item.children"
      :key="child.path"
      :item="child"
      @menu-click="handleClick"
    />
  </el-submenu>

  <el-menu-item v-else :index="item.path" @click="handleClick(item)">
    <i :class="item.icon" v-if="item.icon"  class="menu-icon"></i>
    <span>{{ item.name }}</span>
  </el-menu-item>
</template>

<script>
export default {
  name: "MenuItem",
  props: {
    item: { type: Object, required: true }
  },
  methods: {
    handleClick(item) {
      this.$emit("menu-click", item.path || item);
    }
  }
};
</script>

<style lang="less" scoped>
.menu-icon {
  font-size: 16px;
  margin-right: 8px;
  display: inline-block;
  width: 20px;
  text-align: center;
  color: inherit;
}
</style>