<template>
  <div class="layout">
    <!-- 设置密码弹框 -->
    <SetPasswordModal
      v-if="showSetPassword"
      @confirm="handleSetPassword"
      @close="setShowSetPassword(false)"
    />

    <!-- 锁屏界面 -->
    <LockScreen
      v-if="isLocked && !showUnlockPage"
      :avatar="avatar"
      @unlockClick="showUnlockPage = true"
    />

    <!-- 输入密码解锁页面 -->
    <UnlockPage
      v-if="isLocked && showUnlockPage"
      :avatar="avatar"
      @unlock="handleUnlock"
      @back="showUnlockPage = false"
    />
    <!-- 左侧菜单栏 -->
    <div class="left-side" :style="{ width: leftWidth + 'px' }">
      <MyMenu class="menu" :isCollapse="isCollapse" />
    </div>
    <!-- 右侧菜单栏 -->
    <div class="right-side" :style="{ left: leftWidth + 'px' }">
      <Content
        class="content"
        @changeMenu="changeMenu"
        :isCollapse="isCollapse"
        :class="{ isActive: isCollapse }"
      />
    </div>
  </div>
</template>

<script>
import SetPasswordModal from "@/components/LockScreen/SetPasswordModal.vue";
import LockScreen from "@/components/LockScreen/LockScreen.vue";
import UnlockPage from "@/components/LockScreen/UnlockPage.vue";
import { mapState, mapActions } from "vuex";
import avatar from "@/assets/horse.png";
import Content from "./MyContent.vue";
import MyMenu from "./MyMenu.vue";
export default {
  components: {
    MyMenu,
    Content,
    SetPasswordModal,
    LockScreen,
    UnlockPage,
  },
  data() {
    return {
      isCollapse: false,
      leftWidth: 200, // 初始宽度200px
      showUnlockPage: false,
      avatar,
    };
  },
  computed: {
    // 数组形式 - 同名映射
    ...mapState("LockModule", ["isLocked", "LockPassword", "showSetPassword"]),
  },
  mounted() {
    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.handleKeydown);
  },
  methods: {
    // 模块 actions
    ...mapActions("LockModule", [
      "lock",
      "unlock",
      "SetLockPassword",
      "setShowSetPassword",
    ]),
    handleKeydown(e) {
      if (e.altKey && e.key.toLowerCase() === "l") {
        if (!this.isLocked) {
          this.setShowSetPassword(true);
        }
      }
    },
    handleSetPassword(pwd) {
      this.SetLockPassword(pwd);
      this.setShowSetPassword(false);
      this.lock();
    },
    handleUnlock(inputPwd) {
      if (!inputPwd) return this.$message.warning("请输入密码");
      if (inputPwd === this.LockPassword) {
        this.unlock();
        this.showUnlockPage = false;
      } else {
        this.$message.error("密码错误");
      }
    },
    /**
     * 父组件接收事件
     */
    changeMenu() {
      this.isCollapse = !this.isCollapse;
      this.leftWidth = this.isCollapse ? 64 : 200;
    },
  },
};
</script>

<style lang="less" scoped>
.layout {
  position: relative;

  height: 100vh;
  overflow: hidden;
  background-color: #fff;
  .left-side {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    transition: width 0.4s ease;
    box-sizing: border-box;
  }
  .right-side {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    transition: left 0.4s ease;
    box-sizing: border-box;
    overflow: auto;
    border-left: 1px solid #ebeef5; /* 新增左侧边框 */
  }
}
</style>