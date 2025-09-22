<template>
  <el-menu
    :default-active="$route.path"
    class="el-menu-vertical-demo"
    router
    :collapse="isCollapse"
  >
    <el-menu-item disabled>
      <div
        style="
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          background: white;
          border-radius: 50%;
          margin-right: 8px;
        "
      >
        <img
          src="@/assets/horse.png"
          style="width: 24px; height: 24px; object-fit: cover"
        />
      </div>
      <span slot="title">后台管理系统</span>
    </el-menu-item>
    <!-- 正确的 v-for 使用方式 -->
    <template v-for="item in menu_list">
      <el-menu-item
        v-if="!item.children || item.children.length === 0"
        :index="item.path"
        :key="item.path"
        @click="updateMenu(item)"
      >
        <i :class="item.icon"></i>
        <span slot="title">{{ item.name }}</span>
      </el-menu-item>

      <el-submenu v-else :key="item.path" :index="item.path">
        <template slot="title">
          <i :class="item.icon"></i>
          <span slot="title">{{ item.name }}</span>
        </template>
        <el-menu-item-group>
          <el-menu-item
            v-for="(child, index) in item.children"
            :key="index"
            :index="child.path"
            @click="updateMenu(child.path)"
          >
            <i :class="['menu-icon', child.icon]"></i>
            <span slot="title">{{ child.name }}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </template>
  </el-menu>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  props: ["isCollapse"],
  data() {
    return {};
  },
  computed: {
    ...mapGetters("PermissionModule", ["menuPermissions"]),
    menu_list() {
      return this.menuPermissions || [];
    },
  },
  mounted() {
    // 初始化时也根据当前路由更新菜单
    this.updateMenuFromRoute(this.$route);
  },
  methods: {
    ...mapActions("MenuStateModule", ["setCurrentMenuaddTabMenu"]),
    // 新增方法：根据路由更新菜单状态
    updateMenuFromRoute(route) {
      const matchedRoute = route.path;
      this.setCurrentMenuaddTabMenu(matchedRoute);
    },
    updateMenu(path) {
      //触发action
      this.setCurrentMenuaddTabMenu(path);
    },
  },
};
</script>

<style lang="less" scoped>
.el-menu {
  border-right: 0px;
  .el-menu-item.is-active {
    background-color: #e0effc !important; //修改激活颜色
  }
  // 禁用项样式
  ::v-deep .el-menu-item.is-disabled {
    opacity: 1; // 保持不透明
    // cursor: default; // 保持默认光标
    cursor: pointer; // 手型光标
    background-color: transparent !important; // 透明背景
    color: inherit !important; // 继承文字颜色

    &:hover {
      background-color: transparent !important; // 悬停时也透明
    }
  }
}
::v-deep(.el-menu-item-group__title) {
  padding: 0;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.menu-icon {
  font-size: 16px;
  margin-right: 8px;
  display: inline-block;
  width: 20px;
  text-align: center;
  color: inherit;
}
</style>