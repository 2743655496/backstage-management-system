<template>
  <div class="icon-dropdown" ref="dropdown">
    <!-- 图标按钮 -->
    <button class="circle-btn" @click.stop="handleIconClick">
      <img src="@/assets/horse.png" alt="用户头像" />
    </button>

    <!-- 下拉菜单带动画 -->
    <transition name="fade-slide">
      <div v-if="isOpen" class="user-dropdown">
        <div class="profile-header">
          <img :src="user.avatar" alt="avatar" class="avatar" />
          <div class="info">
            <div class="name">{{ user.name }}</div>
            <div class="email">{{ user.email }}</div>
            <span v-if="user.isPro" class="badge">Pro</span>
          </div>
        </div>

        <ul class="menu">
          <li @click="goToDocs">📄 文档</li>
          <li @click="goToGithub">🐙 GitHub</li>
          <li @click="goToHelp">❓ 问题 & 帮助</li>
          <li @click="lockScreen">🔒 锁定屏幕 <span class="shortcut">Alt + L</span></li>
          <li @click="logout">🚪 退出登录</li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "IconDropdown",
  data() {
    return {
      isOpen: false,
      user: {
        name: "Vben",
        email: "ann.vben@gmail.com",
        avatar: require("@/assets/logo.png"),
        isPro: true,
      },
    };
  },
  mounted() {
    window.addEventListener("blur", this.closeDropdown);
  },
  beforeDestroy() {
    window.removeEventListener("blur", this.closeDropdown);
  },
  methods: {
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
      this.$router.push("/docs");
      this.closeDropdown();
    },
    goToGithub() {
      window.open("https://github.com/your-repo", "_blank");
      this.closeDropdown();
    },
    goToHelp() {
      this.$router.push("/help");
      this.closeDropdown();
    },
    lockScreen() {
      console.log("锁定屏幕");
      this.closeDropdown();
    },
    logout() {
      this.$router.push("/auth/login");
      this.closeDropdown();
    },
  },
};
</script>

<style scoped>
.icon-dropdown {
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
  top: 48px;
  right: 0;
  width: 260px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  font-family: "Segoe UI", "PingFang SC", sans-serif;
  z-index: 1000;
  overflow: hidden;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 16px;
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
