<template>
  <el-container class="my-el-container">
    <el-header
      style="font-size: 12px"
      class="my-el-header"
      :class="{ immersive: isImmersive }"
    >
      <el-row class="rowone" v-show="!isImmersive">
        <button @click="changeMenu" class="btn" v-if="!shouldHideMenuButton">
          <i v-if="!isCollapse" class="el-icon-s-fold"></i>
          <i v-else class="el-icon-s-unfold"></i>
        </button>
        <button class="btn" @click="refreshView">
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
        <button class="btn-radius" @click="handleClick">
          <transition name="fade">
            <i
              :class="[
                isLightOn ? 'el-icon-sunny' : 'el-icon-moon',
                { 'reverse-spin': isSpinning && isLightOn },
              ]"
              key="icon"
            ></i>
          </transition>
        </button>
        <ButtonIconDropdown
          :iconList="languages"
          triggerIconClass="iconfont icon-yuyan"
          :selectedIcon="currentLanguage"
          @select="changeLang"
        />
        <button class="btn-radius" @click="toggleFullscreen">
          <i
            :class="
              isFullscreen ? 'iconfont icon-suoxiao' : 'iconfont icon-fangda'
            "
          ></i>
        </button>

        <button class="btn-radius">
          <i class="el-icon-message-solid"></i>
        </button>
        <ButtonImageDropdown />
      </el-row>
      <Tabs
        @refresh-view="refreshView"
        @fangda-suoxiao="fangda_suoxiao"
        :isImmersive="isImmersive"
      />
    </el-header>

    <el-main :class="{ immersive: isImmersive }">
      <router-view :key="viewKey"></router-view>
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
    ...mapGetters("LightModule", ["isLightOn"]),
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
      viewKey: 0, // 用来强制刷新 router-view
      isFullscreen: false, // 是否全屏
      isImmersive: false, // ⭐ 新增：沉浸模式
      isSpinning: false,
    };
  },
  watch: {
    shouldHideMenuButton(val) {
      if (val && !this.isCollapse) {
        if (!this.isImmersive) {
          this.$emit("changeMenu"); // 触发父组件折叠逻辑
        }
      }
    },
  },
  mounted() {
    this.checkScreenWidth();
    window.addEventListener("resize", this.checkScreenWidth);

    // 监听全屏变化
    document.addEventListener("fullscreenchange", this.fullscreenListener);
    document.addEventListener(
      "webkitfullscreenchange",
      this.fullscreenListener
    );
    document.addEventListener("mozfullscreenchange", this.fullscreenListener);
    document.addEventListener("MSFullscreenChange", this.fullscreenListener);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkScreenWidth);
    document.removeEventListener("fullscreenchange", this.fullscreenListener);
    document.removeEventListener(
      "webkitfullscreenchange",
      this.fullscreenListener
    );
    document.removeEventListener(
      "mozfullscreenchange",
      this.fullscreenListener
    );
    document.removeEventListener("MSFullscreenChange", this.fullscreenListener);
  },
  methods: {
    ...mapActions("LightModule", ["toggleLight"]),
    ...mapActions("MenuStateModule", ["setCurrentMenuaddTabMenu"]),
    ...mapActions("chartRenderKey", ["triggerChartRemount"]),
    checkScreenWidth() {
      this.shouldHideMenuButton = window.innerWidth <= 776;
    },
    /**
     * 自定义事件，触发父组件里的事件，折叠左侧菜单栏
     */
    changeMenu() {
      this.$emit("changeMenu");
      if (this.$route.path === "/dashboard/analysis") {
        this.triggerChartRemount();
      }
    },
    // 面包屑菜单跳转
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
    /**
     * 刷新
     */
    refreshView() {
      this.viewKey++;
      // 如果你希望在工作台刷新时顺带重渲染图表（和你 changeMenu 逻辑类似）
      if (this.$route.path === "/dashboard/analysis") {
        this.triggerChartRemount();
      }
    },
    // 沉浸模式
    fangda_suoxiao() {
      this.isImmersive = !this.isImmersive;
      // 通知父级（Layout.vue）隐藏/显示侧边栏
      this.$emit("fangda-suoxiao", !this.isImmersive);

      if (this.shouldHideMenuButton && !this.isCollapse) {
        if (!this.isImmersive) {
          this.$emit("changeMenu"); // 触发父组件折叠逻辑
        }
      }
    },
    //点灯开灯
    handleClick() {
      if (this.isLightOn) {
        // 太阳图标触发反向旋转
        this.isSpinning = true;
        setTimeout(() => {
          this.toggleLight(); // 每次点击切换 isLightOn
          this.isSpinning = false;
        }, 100); // 动画持续时间
      } else {
        // 月亮直接切换为太阳，无动画
        this.toggleLight(); // 每次点击切换 isLightOn
      }
    },
    /**
     * 全屏功能
     */
    fullscreenListener() {
      this.isFullscreen = !!(
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
      );
    },
    toggleFullscreen() {
      if (!this.isFullscreen) {
        // 进入全屏
        const el = document.documentElement;
        if (el.requestFullscreen) el.requestFullscreen();
        else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
        else if (el.mozRequestFullScreen) el.mozRequestFullScreen();
        else if (el.msRequestFullscreen) el.msRequestFullscreen();
      } else {
        //  退出全屏
        if (document.exitFullscreen) document.exitFullscreen();
        else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
        else if (document.mozCancelFullScreen) document.mozCancelFullScreen();
        else if (document.msExitFullscreen) document.msExitFullscreen();
      }
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
  /* 太阳反向旋转动画 */
  .reverse-spin {
    animation: reverseRotate 0.4s ease;
  }
  @keyframes reverseRotate {
    0% {
      transform: rotate(0deg);
    }
    40% {
      transform: rotate(40deg);
    } /* 40% of 360° */
    100% {
      transform: rotate(0deg);
    }
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
    // height: 82px; // 默认高度（50px rowone + 32px tabs）
    // transition: height 0.3s ease;
    &.immersive {
      height: 32px !important; // ⭐ 只保留 Tabs 的高度
    }
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
    background-color: #f5f7fa;
    display: block;
    flex: 1;
    flex-basis: auto;
    overflow: auto;
    box-sizing: border-box;
    padding: 20px;
    margin: 24px 0px 0px 0px; /* 上右下左 */
    &.immersive {
      margin: 0px 0px 0px 0px !important; // ⭐ 只保留 Tabs 的高度
    }
  }
  .el-main::-webkit-scrollbar {
    width: 8px;
  }
  .el-main::-webkit-scrollbar-thumb {
    background-color: #bbb;
    border-radius: 4px;
  }
  .el-main::-webkit-scrollbar-track {
    background-color: #f5f5f5;
  }
}
</style>