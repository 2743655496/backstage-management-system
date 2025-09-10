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
            <li @click="goToDocs">📄 文档</li>
            <li @click="goToGithub">🐙 GitHub</li>
            <li @click="goToHelp">❓ 问题 & 帮助</li>
            <li @click="lockScreen">
              🔒 锁定屏幕 <span class="shortcut">Alt + L</span>
            </li>
            <li @click="logoutdialogVisible = true">
              🚪 退出登录<span class="shortcut">Alt + Q</span>
            </li>
          </ul>
        </div>
      </transition>
    </div>
    <el-dialog title="提示" :visible.sync="logoutdialogVisible" width="30%" append-to-body>
      <span>是否退出登录？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="logoutdialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="logout">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { toLogout } from "@/api/index.js";
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
    handleKeydown(event) {
      // 检查是否按下 Alt + Q
      if (event.altKey && event.key.toLowerCase() === "q") {
        event.preventDefault(); // 阻止默认行为（可选）
        this.logoutdialogVisible = true
        // this.logout(); // 调用退出方法
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
      // 调用后端退出接口
      toLogout()
        .then(() => {
          // 清除 Vuex 中的用户信息
          this.$store.commit("LoginModule/clearUser");

          // 清除前端 Cookie（如果你用 js-cookie 管理）
          // this.$cookies.remove('access_token');
          // this.$cookies.remove('refresh_token');

          // 跳转到登录页
          this.$router.push("/auth/login");
        })
        .catch((error) => {
          console.error("退出登录失败:", error);
          this.$message.error("退出登录失败，请稍后重试");
        })
        .finally(() => {
          this.closeDropdown();
        });
    },
  },
};
</script>

<style scoped>
::v-deep .el-dialog {
  margin-top: 0 !important;
  top: 40% !important;
  transform: translateY(-50%) !important;}
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
  margin-top: 8px;
  right: 10px;
  width: 260px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  font-family: "Segoe UI", "PingFang SC", sans-serif;
  z-index: 1000;
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
