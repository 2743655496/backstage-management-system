<template>
  <div class="container">
    <div class="layout" :class="layoutMode">
      <div class="content center-content">
        <router-view></router-view>
      </div>
      <div class="background" :style="backgroundStyle">
        <div v-if="layoutMode !== 'center'">
          <img
            src="@/assets/svg/87.svg"
            alt="Logo"
            width="200px"
            height="200px"
            class="logoimg"
          />
          <p style="margin-top: 10px; font-size: 16px; color: #333">
            {{ $t('login.background_content') }}
          </p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="icon-buttons">
        <div class="icon-btn-diaoseban">
          <ColorPalette
            @select="handleColorSelect"
            :current_color="gradientColor"
          />
        </div>
        <div class="icon-btn-dropdown min-concealment">
          <IconDropdown
            :iconList="layout_position"
            :triggerIconClass="current_layout_position"
            :selectedIcon="current_layout_position"
            @select="handleSelect"
          />
        </div>
        <div>
          <IconDropdown
            class="icon-btn-dropdown"
            :iconList="languages"
            triggerIconClass="iconfont icon-yuyan"
            :selectedIcon="currentLanguage"
            @select="changeLang"
          />
        </div>
        <span class="icon-btn">
          <transition name="fade">
            <i
              :class="[
                isDay ? 'el-icon-sunny' : 'el-icon-moon',
                'switch-icon',
                { 'reverse-spin': isSpinning && isDay },
              ]"
              @click="handleClick"
              key="icon"
            ></i>
          </transition>
        </span>
      </div>
    </div>

    <div class="header">
      <div
        style="
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          margin-right: 8px;
        "
      >
        <img
          src="@/assets/horse.png"
          style="width: 32px; height: 32px; object-fit: cover"
        />
      </div>
      <span slot="title" class="title">Vue2 My Admin</span>
    </div>
  </div>
</template>
 
<script>
import IconDropdown from "@/components/IconDropdown.vue";
import ColorPalette from "@/components/Login/ColorPalette.vue";

import { mapGetters, mapActions } from "vuex";
export default {
  name: "Login",
  components: { IconDropdown, ColorPalette },
  data() {
    return {
      current_color:localStorage.getItem("light_color") ||"white",
      layoutMode: localStorage.getItem("layoutMode") || "right", // 初始布局
      gradientColor: localStorage.getItem("gradientColor") || "#bddff5",
      isDay: true,
      isSpinning: false,
      current_layout_position:
        localStorage.getItem("layout_position_icon") ||
        "iconfont icon-buju_juyou",
      layout_position: [
        { name: "居左", icon: "iconfont icon-buju_juzuo" },
        {
          name: "居中",
          icon: "iconfont icon-Edit_chuizhijuzhong_margin_linear",
        },
        { name: "居右", icon: "iconfont icon-buju_juyou" },
      ],
    };
  },
  computed: {
    ...mapGetters("LanguageModule", ["currentLanguage", "languages"]),
    backgroundStyle() {
      return {
        background: `linear-gradient(155deg, ${this.current_color}, ${this.gradientColor} 50%, ${this.current_color})`,
      };
    },
  },
  mounted() {
    // checkAuth()
  },
  methods: {
    ...mapActions("LanguageModule", ["changeLanguage"]),
    /**
     * 切换语言
     */
    changeLang(command) {
      console.log(command)
      this.changeLanguage(command.name);
    },
    handleSelect(item) {
      if (item.name == "居左") {
        this.layoutMode = "left";
      } else if (item.name == "居中") {
        this.layoutMode = "center";
        // 这里可以根据需求设置居中的逻辑
      } else if (item.name == "居右") {
        this.layoutMode = "right";
      }
      this.current_layout_position = item.icon;

      localStorage.setItem(
        "layout_position_icon",
        this.current_layout_position
      );
      localStorage.setItem("layoutMode", this.layoutMode); // 存储为字符串
    },
    handleClick() {
      if (this.isDay) {
        // 太阳图标触发反向旋转
        this.isSpinning = true;
        setTimeout(() => {
          this.isDay = false;
          this.isSpinning = false;
        }, 200); // 动画持续时间
        this.current_color = "white"
        localStorage.setItem("light_color", this.current_color); // 存储为字符串
      } else {
        // 月亮直接切换为太阳，无动画
        this.isDay = true;
        this.current_color = "#000000"
        localStorage.setItem("light_color", this.current_color); // 存储为字符串
      }
    },
    handleColorSelect(color) {
      this.gradientColor = color;
      // 可在此处执行其他逻辑，如修改主题颜色等
      localStorage.setItem("gradientColor", this.gradientColor); // 存储为字符串
    },
  },
};
</script>
 
<style lang="less" scoped>
html,
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  overflow-x: hidden;
}
*,
*::before,
*::after {
  box-sizing: inherit;
}
.container {
  .layout {
    display: flex;
    width: 100%;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
  }

  /* 背景区域 */
  .background {
    display: flex;
    background: linear-gradient(to right, #74ebd5, #9face6);
    z-index: 0;
    flex-direction: column; /* 关键！让子元素垂直排列 */
    justify-content: center;
    align-items: center;
    .logoimg {
      animation: bounce 4s infinite ease-in-out;
      transform-origin: center bottom;
    }
    @keyframes bounce {
      0%,
      100% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-40px); /* 跳得更高 */
      }
    }
  }

  /* 内容区域 */
  .content {
    z-index: 2;
    background-color: rgba(255, 255, 255, 0.95);
    font-size: 24px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
    min-height: 100vh;
  }
  @media (max-width: 1300px) {
    .center-content {
      width: 50% !important;
      left: 0;
      right: auto;
    }
  }
  @media (max-width: 1000px) {
    .background {
      display: none;
    }

    .content {
      width: 100% !important;
      left: 0;
      right: auto;
    }
  }

  /* 居左布局：内容左，背景右 */
  .layout.left {
    flex-direction: row;
  }
  .layout.left .content {
    width: 36%;
  }
  .layout.left .background {
    width: 64%;
  }

  /* 居右布局：内容右，背景左 */
  .layout.right {
    flex-direction: row-reverse;
  }
  .layout.right .content {
    width: 36%;
  }
  .layout.right .background {
    width: 64%;
  }

  /* 居中布局：背景在下，内容覆盖在上 */
  .layout.center {
    justify-content: center;
    position: relative;
  }

  .layout.center .background {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
  }

  .layout.center .content {
    width: 36%;
    z-index: 2;
    background-color: rgba(255, 255, 255, 0.95);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  }
  /* 标题 */
  .header {
    position: absolute;
    z-index: 3;
    top: 20px;
    left: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    .title {
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 20px;
      font-weight: 300;
      letter-spacing: 0.5px;
      line-height: 1.6;
    }
  }
  /* 控制按钮 */
  .card {
    width: auto;
    position: absolute;
    top: 20px;
    right: 30px;
    z-index: 3;
    padding: 10px 28px;
    border-radius: 50px;
    background-color: #f2f2f2;
    display: flex;
    justify-content: center;
    align-items: center;
    @media (max-width: 770px) {
      .icon-buttons .icon-btn-diaoseban,
      .icon-buttons .icon-btn-dropdown.min-concealment {
        display: none;
      }
    }

    .icon-buttons {
      display: flex;
      gap: 20px;
    }

    .switch-icon {
      cursor: pointer;
      // transition: transform 0.3s ease;
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

    .icon-btn {
      font-size: 14px;
      cursor: pointer;
      color: #494949; /* 默认浅灰色 */
    }
    icon-btn-dropdown {
      font-size: 14px;
      cursor: pointer;
      color: #494949; /* 默认浅灰色 */
    }
    icon-btn-diaoseban {
      font-size: 14px;
      cursor: pointer;
    }

    .icon-btn:hover {
      color: #1890ff;
    }
  }
}
</style>

