<template>
  <!-- <div>123</div> -->
  <el-menu
    default-active="/"
    class="el-menu-vertical-demo"
    background-color="#4a73be"
    text-color="#fff"
    router
    active-text-color="#ffd04b"
    :collapse="isCollapse"
  >
    <el-menu-item>
      <div style="
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  margin-right: 8px;
">
  <img 
    src="@/assets/horse.png" 
    style="
      width: 24px;
      height: 24px;
      object-fit: cover;
    "
  />
</div>
      <span slot="title">后台管理系统</span>
    </el-menu-item>
    <el-menu-item index="/">
      <i class="el-icon-menu"></i>
      <span slot="title">首页</span>
    </el-menu-item>
    <el-menu-item index="/goods">
      <i class="el-icon-menu"></i>
      <span slot="title">商品管理</span>
    </el-menu-item>
    <el-submenu index="/params">
      <template slot="title">
        <i class="el-icon-location"></i>
        <span slot="title">规格参数</span>
      </template>
      <el-menu-item-group>
        <el-menu-item index="3-1">选项1</el-menu-item>
        <el-menu-item index="3-2">选项2</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="/order">
      <i class="el-icon-setting"></i>
      <span slot="title">订单管理</span>
    </el-menu-item>
    <el-menu-item index="/user">
      <i class="el-icon-setting"></i>
      <span slot="title">用户管理</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  props:["isCollapse"],
  data() {
    return {
    };
  },
  methods: {},
};
</script>

<style lang="less" scoped>
.el-menu {
  border-right: 0px;
  .el-menu-item.is-active {
    background-color: #054476 !important;
  }
  
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>