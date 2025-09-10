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
        :index="item.router_path"
        :key="item.router_path"
        @click="updateMenu(item)"
      >
        <i :class="item.icon"></i>
        <span slot="title">{{ item.name }}</span>
      </el-menu-item>

      <el-submenu v-else :key="item.router_path" :index="item.router_path">
        <template slot="title">
          <i :class="item.icon"></i>
          <span slot="title">{{ item.name }}</span>
        </template>
        <el-menu-item-group>
          <el-menu-item
            v-for="(child, index) in item.children"
            :key="child.router_path"
            :index="child.router_path"
            @click="updateMenu(item, index)"
          >
            {{ child.name }}
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </template>
  </el-menu>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: ["isCollapse"],
  data() {
    return {
      menu_list: [
        {
          router_path: "/",
          name: this.$t("menu.home"),
          icon: "el-icon-menu",
          children: [],
        },
        {
          router_path: "/goods",
          name: this.$t("menu.goods"),
          icon: "el-icon-s-goods",
          children: [],
        },
        {
          router_path: "/category",
          name: this.$t("menu.params"),
          icon: "el-icon-document",
          children: [
            {
              router_path: "/category",
              name: this.$t("menu.specification_category"),
            },
            {
              router_path: "/params",
              name: "规格参数",
            },
          ],
        },
        {
          router_path: "/order",
          name: "订单管理",
          icon: "el-icon-s-order",
          children: [],
        },
        {
          router_path: "/user",
          name: "用户管理",
          icon: "el-icon-user",
          children: [],
        },
      ],
    };
  },
  mounted() {
    // 初始化时也根据当前路由更新菜单
    this.updateMenuFromRoute(this.$route);
  },
  methods: {
    ...mapActions("MenuStateModule", ["setCurrentMenu"]),
    // 新增方法：根据路由更新菜单状态
    updateMenuFromRoute(route) {
      // 这里需要根据你的实际路由结构来实现
      // 假设你的菜单数据有一个router_path字段与路由匹配
      const matchedRoute = route.path;
      // 你需要遍历你的菜单项，找到与当前路由匹配的项
      // 这里只是一个示例，你需要根据你的实际菜单数据结构来实现
      const findMatchingMenu = (menuItems) => {
        for (let i = 0; i < menuItems.length; i++) {
          const item = menuItems[i];
          if (item.children && item.children.length > 0) {
            const found = findMatchingMenu(item.children);
            if (found) {
              // 返回父级项和子级索引
              return { item, childIndex: found.index, isChild: true };
            }
          }
          if (item.router_path === matchedRoute) {
            return { item, index: i };
          }
        }
        return null;
      };

      // 假设你的菜单数据存储在某个地方，比如Vuex中或从API获取
      // 这里需要根据你的实际情况获取菜单数据
      const menuData = this.menu_list; // 假设菜单数据存在这里

      if (menuData) {
        const matchedMenu = findMatchingMenu(menuData);
        if (matchedMenu.isChild) {
          // 更新当前菜单状态
          this.setCurrentMenu([matchedMenu.item, matchedMenu.childIndex]);
        } else {
          this.setCurrentMenu([matchedMenu.item, matchedMenu.index]);
        }
      }
    },
    updateMenu(menu, index) {
      //触发action
      this.setCurrentMenu([menu, index]);
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
</style>