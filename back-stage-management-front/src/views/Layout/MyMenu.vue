<template>
  <div class="sidebar-menu">
    <!-- 顶部 logo 区域 -->
    <div class="menu-header">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
        :collapse="isCollapse"
        :text-color="textColor"
        :active-text-color="activeColor"
        :background-color="backgroundColor"
      >
        <el-menu-item disabled>
          <div class="logo">
            <img src="@/assets/images/horse.png" />
          </div>
          <span :style="{ color: textColor }">后台管理系统</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 菜单项区域 -->
    <div class="menu-scroll">
      <el-menu
        v-if="isLightOn"
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
        :collapse="isCollapse"
        :text-color="textColor"
        :active-text-color="activeColor"
      >
        <menu-item
          v-for="item in menu_list"
          :key="item.path"
          :item="item"
          @menu-click="updateMenu"
        />
      </el-menu>
      <el-menu
        v-else
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
        :collapse="isCollapse"
        :text-color="textColor"
        :active-text-color="activeColor"
        :background-color="backgroundColor"
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
    ...mapGetters("LightModule", [
      "isLightOn",
      "backgroundColor",
      "textColor",
      "activeColor",
      "hoverColor",
    ]),
    menu_list() {
      return this.menuPermissions || [];
    },
  },
  mounted() {
    document.body.style.setProperty("--hover-color", this.hoverColor);
    this.updateMenuFromRoute(this.$route);
  },
  watch: {
    hoverColor(val) {
      document.body.style.setProperty("--hover-color", val);
    },
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
/* ===========================
   外层统一背景（主题切换核心）
   =========================== */
.sidebar-menu {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: v-bind(backgroundColor);

  /* 顶部区域同步背景 */
  .menu-header {
    flex-shrink: 0;
    position: sticky;
    top: 0;
    z-index: 10;
    background-color: v-bind(backgroundColor);

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

  /* ===========================
     菜单滚动区域
     =========================== */
  .menu-scroll {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: v-bind(backgroundColor);

    ::v-deep .el-menu,
    ::v-deep .el-submenu__title,
    ::v-deep .el-menu-item {
      background-color: transparent !important;
    }

    ::v-deep .el-menu-item:hover,
    ::v-deep .el-submenu__title:hover {
      background-color: v-bind(hoverColor) !important;
    }

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

/* logo 样式 */
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

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
}
</style>

<style lang="less">
/* popup 根节点背景 */
// body .el-menu--popup,
// body .el-menu--popup-right-start {
//   background-color: var(--bg-color) !important;
// }

/* popup hover（关键） */
/* 折叠 popup hover */
body .el-menu--popup .el-menu-item:hover,
body .el-menu--popup-right-start .el-menu-item:hover {
  background-color: var(--hover-color) !important;
  // color: var(--active-color) !important;
}
</style>
