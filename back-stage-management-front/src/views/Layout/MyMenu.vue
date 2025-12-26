<template>
  <div class="sidebar-menu">
    <!-- 顶部 logo 区域固定 -->
    <div class="menu-header">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
        :collapse="isCollapse"
      >
        <el-menu-item disabled>
          <div class="logo">
            <img src="@/assets/images/horse.png" />
          </div>
          <span slot="title">后台管理系统</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 菜单项区域可滚动 -->
    <div class="menu-scroll">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
        :collapse="isCollapse"
      >
        <menu-item
          v-for="item in menu_list"
          :key="item.path"
          :item="item"
          @menu-click="updateMenu"
        />
      </el-menu>
    </div>
  </div>
</template>

<script>
import MenuItem from "@/components/Layout/MenuItem.vue";
import { mapActions, mapGetters } from "vuex";

export default {
  name: "SidebarMenu",
  components: { MenuItem },
  props: ["isCollapse"],
  computed: {
    ...mapGetters("PermissionModule", ["menuPermissions"]),
    menu_list() {
      return this.menuPermissions || [];
    },
  },
  mounted() {
    this.updateMenuFromRoute(this.$route);
  },
  methods: {
    ...mapActions("MenuStateModule", ["setCurrentMenuaddTabMenu"]),
    updateMenuFromRoute(route) {
      this.setCurrentMenuaddTabMenu(route.path);
    },
    updateMenu(path) {
      this.setCurrentMenuaddTabMenu(path);
    },
  },
};
</script>

<style lang="less" scoped>
.sidebar-menu {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #fff;

  .menu-header {
    .el-menu-item {
      margin-left: -5px;
      height: 56px;
      font-size: 14px;
      color: #303133;
      cursor: pointer;
      transition: border-color 0.3s, background-color 0.3s, color 0.3s;
      box-sizing: border-box;
    }
    flex-shrink: 0;
    position: sticky;
    top: 0;
    z-index: 10;
    background-color: #fff;
    border-bottom: 1px solid #eee;
  }

  .menu-scroll {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;

    &::-webkit-scrollbar {
      width: 6px;
    }
    &::-webkit-scrollbar-thumb {
      background-color: #ccc;
      border-radius: 3px;
    }
    &::-webkit-scrollbar-track {
      background-color: #f5f5f5;
    }
  }
}

.logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  margin-right: 8px;

  img {
    width: 30px;
    height: 30px;
    object-fit: cover;
  }
}

.el-menu {
  border-right: 0px;

  .el-menu-item.is-active {
    background-color: #e0effc !important;
  }

  ::v-deep .el-menu-item.is-disabled {
    opacity: 1;
    cursor: pointer;
    background-color: transparent !important;
    color: inherit !important;

    &:hover {
      background-color: transparent !important;
    }
  }
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
}
</style>
