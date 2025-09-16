<template>
  <el-container class="my-el-container">
    <el-header style="font-size: 12px" class="my-el-header">
      <el-row class="rowone">
        <button @click="changeMenu" class="btn" v-if="!shouldHideMenuButton">
          <i v-if="!isCollapse" class="el-icon-s-fold"></i>
          <i v-else class="el-icon-s-unfold"></i>
        </button>
        <button class="btn">
          <i class="el-icon-refresh"></i>
        </button>
        <el-breadcrumb
          separator-class="el-icon-arrow-right"
          class="icon-el-breadcrumb"
        >
          <template v-for="(item, index) in CurrentMenu">
            <!-- 不是最后一项，有链接 -->
            <el-breadcrumb-item
              v-if="index < CurrentMenu.length - 1"
              :key="index"
              @click.native="navigateTo(item)"
            >
              {{ item.name }}
            </el-breadcrumb-item>

            <!-- 最后一项，没有链接 -->
            <el-breadcrumb-item v-else :key="index + 'last'">
              {{ item.name }}
            </el-breadcrumb-item>
          </template>
        </el-breadcrumb>
        <div class="header-right"></div>
        <button class="btn-radius">
          <i class="el-icon-setting"></i>
        </button>
        <button class="btn-radius">
          <!-- <i class="el-icon-sunny"></i> -->
          <i class="el-icon-moon"></i>
        </button>
        <ButtonIconDropdown
          :iconList="languages"
          triggerIconClass="iconfont icon-yuyan"
          :selectedIcon="currentLanguage"
          @select="changeLang"
        />
        <button class="btn-radius">
          <i class="iconfont icon-fangda"></i>
          <!-- <i class="iconfont icon-suoxiao"></i> -->
        </button>
        <button class="btn-radius">
          <i class="el-icon-message-solid"></i>
        </button>
        <!-- <button class="circle-btn">
          <img src="@/assets/horse.png" alt="用户头像" />
        </button> -->
        <ButtonImageDropdown />
      </el-row>
      <Tabs />
    </el-header>

    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script>
import Tabs from "@/components/Layout/MyTabs.vue";
import ButtonIconDropdown from "@/components/ButtonIconDropdown.vue";
import ButtonImageDropdown from "@/components/Layout/ButtonImageDropdown.vue";
import { mapState, mapGetters, mapActions } from "vuex";
import navigation from "@/utils/navigation";

export default {
  computed: {
    ...mapGetters("LanguageModule", ["currentLanguage", "languages"]),
    ...mapState("MenuStateModule", ["CurrentMenu"]),
  },
  components: {
    Tabs,
    ButtonIconDropdown,
    ButtonImageDropdown,
  },
  props: ["isCollapse"],
  data() {
    return {
      shouldHideMenuButton: false,
    };
  },
  watch: {
    shouldHideMenuButton(val) {
      if (val && !this.isCollapse) {
        this.$emit("changeMenu"); // 触发父组件折叠逻辑
      }
    },
  },
  mounted() {
    this.checkScreenWidth();
    window.addEventListener("resize", this.checkScreenWidth);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkScreenWidth);
  },
  methods: {
    ...mapActions("MenuStateModule", ["setCurrentMenuaddTabMenu"]),
    checkScreenWidth() {
      this.shouldHideMenuButton = window.innerWidth <= 776;
    },
    /**
     * 自定义事件，触发父组件里的事件
     */
    changeMenu() {
      this.$emit("changeMenu");
    },
    navigateTo(item) {
      const targetPath = item.children?.[0]?.path || item.path;
      this.setCurrentMenuaddTabMenu(targetPath);
      navigation.safePush(this, targetPath);
    },
    /**
     * 切换语言
     */
    changeLang(command) {
      this.changeLanguage(command.name);
    },
  },
};
</script>

<style lang="less" scoped>
.my-el-container {
  height: 100%;
  width: 100%;
  overflow-x: auto; /* 超出时显示横向滚动条 */
  .btn {
    margin-left: 4px;
    padding: 8px 8px;
    background-color: #fff;
    color: #333;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 17px;
  }
  .btn:hover {
    background-color: #f5f5f5;
  }
  .btn-radius {
    margin-left: 4px;
    padding: 8px 8px;
    background-color: #fff;
    color: #333;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 17px;
  }
  .btn-radius:hover {
    background-color: #f5f5f5;
  }

  ::v-deep(.el-header) {
    padding: 0 0px;
  }
  .my-el-header {
    background-color: aqua;
    .rowone {
      height: 50px;
      background-color: #fff;
      display: flex;
      align-items: center; /* 垂直居中 */
      ::v-deep .el-breadcrumb__inner.is-link {
        font-weight: 400;
        text-decoration: none;
        transition: color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
        color: #606266;
        // color: #303133;
      }
      ::v-deep .el-breadcrumb__inner.is-link:hover {
        color: #303133; /* 悬停时变深色 */
        font-weight: 420;
        /* 或者使用主题色，如：color: var(--el-color-primary); */
      }

      ::v-deep .el-breadcrumb__inner {
        font-weight: 450;
        color: #303133;
      }

      .icon-el-breadcrumb {
        font-family: -apple-system, blinkmacsystemfont, "Segoe UI", roboto,
          "Helvetica Neue", arial, "Noto Sans", sans-serif, "Apple Color Emoji",
          "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        font-size: 15px;
        padding-bottom: 1.5px;
        margin-left: 9px;
        // 所有项默认浅灰色
        ::v-deep .el-breadcrumb__item .el-breadcrumb__inner {
          color: #909399;
          font-weight: 400;
          transition: color 0.2s ease;
        }

        // 前面项悬停时变深色 + 手型
        ::v-deep
          .el-breadcrumb__item:not(:last-child):hover
          .el-breadcrumb__inner {
          color: #303133;
          font-weight: 450;
          cursor: pointer;
        }

        // ✅ 最后一项始终为深色
        ::v-deep .el-breadcrumb__item:last-child .el-breadcrumb__inner {
          color: #303133;
          font-weight: 500;
          cursor: default;
        }
      }
      /* 当屏幕宽度 ≤ 768px 时隐藏面包屑 */
      @media (max-width: 768px) {
        .icon-el-breadcrumb {
          display: none;
        }
      }
      .header-right {
        margin-left: auto; // 将元素推到最右侧
      }
    }
  }
  .el-main {
    display: block;
    flex: 1;
    flex-basis: auto;
    overflow: auto;
    box-sizing: border-box;
    padding: 0px;
    margin: 22px 0px 0px 0px; /* 上右下左 */
  }
}
</style>