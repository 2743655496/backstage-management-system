<template>
  <div>
    <div class="icon-dropdown" ref="dropdown">
      <!-- 图标按钮 -->
      <button class="circle-btn" @click.stop="handleIconClick">
        <img
          :src="user.avatar ? user.avatar : require('@/assets/horse.png')"
          alt="用户头像"
        />
      </button>

      <!-- 下拉菜单带动画 -->
      <transition name="fade-slide">
        <div v-if="isOpen" class="user-dropdown">
          <div class="profile-header">
            <img
              :src="user.avatar ? user.avatar : require('@/assets/horse.png')"
              alt="avatar"
              class="avatar"
            />

            <div class="info">
              <div class="name">{{ user.name }}</div>
              <div class="email">{{ user.email }}</div>
              <span v-if="user.isPro" class="badge">Pro</span>
            </div>
          </div>

          <ul class="menu">
            <li
              @click="goToDocs"
              style="display: flex; align-items: center; gap: 5px"
            >
              <span>📄</span> <span>文档</span>
            </li>
            <li
              @click="goToGithub"
              style="display: flex; align-items: center; gap: 5px"
            >
              <svg
                class="icon"
                aria-hidden="true"
                style="width: 12px; height: 12px; margin-left: 2.4"
              >
                <use xlink:href="#icon-GITEE"></use>
              </svg>
              <span>Gitee</span>
            </li>
            <li
              @click="goToHelp"
              style="display: flex; align-items: center; gap: 5px"
            >
              <span>❓</span> <span>问题 & 帮助</span>
            </li>
            <li
              @click="lockScreen"
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <div style="display: flex; align-items: center; gap: 5px">
                <span>🔒</span> <span>锁定屏幕</span>
              </div>
              <span
                class="shortcut"
                style="display: flex; align-items: center; gap: 7.6px"
                ><span>Alt</span><span>L</span></span
              >
            </li>
            <li
              @click="logoutdialogVisible = true"
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <div style="display: flex; align-items: center; gap: 5px">
                <svg
                  class="icon"
                  aria-hidden="true"
                  style="width: 12px; height: 12px; margin-left: 2.3"
                >
                  <use xlink:href="#icon-tuichudenglu"></use></svg
                ><span> 退出登录</span>
              </div>
              <span
                class="shortcut"
                style="display: flex; align-items: center; gap: 5px"
                ><span>Alt</span><span>Q</span></span
              >
            </li>
          </ul>
        </div>
      </transition>
    </div>
    <el-dialog
      title="提示"
      :visible.sync="logoutdialogVisible"
      width="30%"
      append-to-body
    >
      <span>是否退出登录？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="logoutdialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="logout">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "IconDropdown",
  computed: {
    ...mapGetters("LoginModule", ["username", "email", "avatar"]),
    user() {
      return {
        name: this.username,
        email: this.email,
        avatar: this.avatar,
        isPro: true, // 可根据业务逻辑判断是否为 Pro 用户
      };
    },
  },
  data() {
    return {
      logoutdialogVisible: false,
      isOpen: false,
    };
  },
  mounted() {
    window.addEventListener("blur", this.closeDropdown);
    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeDestroy() {
    window.removeEventListener("blur", this.closeDropdown);
    window.removeEventListener("keydown", this.handleKeydown);
  },

  methods: {
    // 模块 actions
    ...mapActions("LockModule", ["setShowSetPassword"]),
    handleKeydown(event) {
      // 检查是否按下 Alt + Q
      if (event.altKey && event.key.toLowerCase() === "q") {
        event.preventDefault(); // 阻止默认行为（可选）
        this.logoutdialogVisible = true;
      }
    },
    handleIconClick() {
      this.isOpen = true;
      setTimeout(() => {
        document.addEventListener("click", this.handleClickOutside, true);
      }, 0);
    },
    closeDropdown() {
      this.isOpen = false;
      document.removeEventListener("click", this.handleClickOutside, true);
    },
    handleClickOutside(event) {
      if (!this.$refs.dropdown.contains(event.target)) {
        this.closeDropdown();
      }
    },
    goToDocs() {
      this.$message.warning("此功能暂未开发，等待更新");
      // this.$router.push("/docs");
      this.closeDropdown();
    },
    goToGithub() {
      this.$message.warning("此功能暂未开发，等待更新");
      // window.open("https://github.com/your-repo", "_blank");
      this.closeDropdown();
    },
    goToHelp() {
      this.$message.warning("此功能暂未开发，等待更新");
      // this.$router.push("/help");
      this.closeDropdown();
    },
    lockScreen() {
      this.setShowSetPassword(true);
      console.log("锁定屏幕");
      this.closeDropdown();
    },
    logout() {
      this.$store.dispatch("LoginModule/logout", {
        router: this.$router,
        message: this.$message,
      });
      this.closeDropdown;
    },
  },
};
</script>

<style scoped>
::v-deep .el-dialog {
  margin-top: 0 !important;
  top: 40% !important;
  transform: translateY(-50%) !important;
}
.icon-dropdown {
  margin-left: 4px;
  margin-right: 4px;
  position: relative;
  display: inline-block;
}

.circle-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background-color: #fff;
  cursor: pointer;
}

.circle-btn:hover {
  background-color: #f5f5f5;
}

.circle-btn img {
  width: 24px;
  height: 24px;
  object-fit: cover;
}

.user-dropdown {
  position: absolute;
  margin-top: 8px;
  right: 10px;
  width: 260px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  font-family: "Segoe UI", "PingFang SC", sans-serif;
  z-index: 4;
  overflow: hidden;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 12px;
}

.info {
  flex: 1;
}

.name {
  font-weight: bold;
  font-size: 16px;
}

.email {
  font-size: 13px;
  color: #888;
}

.badge {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 6px;
  background-color: #0078d4;
  color: white;
  font-size: 12px;
  border-radius: 4px;
}

.menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu li {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.menu li:hover {
  background-color: #f5f5f5;
}

.shortcut {
  float: right;
  color: #aaa;
  font-size: 12px;
}

/* 动画效果 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
