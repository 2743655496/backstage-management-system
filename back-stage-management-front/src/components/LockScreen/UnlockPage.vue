<template>
  <div class="unlock-page">
    <div class="unlock-box">
      <!-- 头像 -->
      <p><img :src="avatar" class="avatar" /></p>
      <!-- 密码输入框 + 眼睛图标 -->
      <div class="input-group">
        <input
          :type="showPassword ? 'text' : 'password'"
          v-model="pwd"
          placeholder="请输入密码"
        />
        <span class="eye-icon" @click="togglePassword">
          <i
            class="el-icon"
            :class="
              showPassword ? 'iconfont icon-yanjing1' : 'iconfont icon-yanjing'
            "
          ></i>
        </span>
      </div>

      <!-- 按钮 -->
      <p><button class="pink-btn" @click="unlock">进入系统</button></p>

      <!-- 底部链接 -->
      <div class="links">
        <span @click="logout"
          ><el-link :underline="false">返回登录</el-link></span
        >
        |
        <span @click="$emit('back')"
          ><el-link :underline="false">返回</el-link></span
        >
      </div>

      <!-- 时间日期 -->
      <div class="time">{{ currentTime }}</div>
      <div class="date">{{ currentDate }}</div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: ["avatar"],
  data() {
    return {
      pwd: "",
      showPassword: false,
      currentTime: "",
      currentDate: "",
    };
  },
  mounted() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    // 模块 actions
    ...mapActions("LockModule", ["clearLock"]),
    unlock() {
      this.$emit("unlock", this.pwd);
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    updateTime() {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString("zh-CN", { hour12: false });
      this.currentDate = now.toLocaleDateString("zh-CN", {
        weekday: "long",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      });
    },
    logout() {
      this.$store.dispatch("LoginModule/logout", {
        router: this.$router,
        message: this.$message,
      });
    },
  },
};
</script>

<style scoped>
.unlock-page {
  position: fixed;
  inset: 0;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.unlock-box {
  text-align: center;
  width: 100%;
  height: 100%;
  padding-top: 150px;
  box-sizing: border-box;
}

.avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
}

.input-group {
  position: relative;
  display: inline-block;
  margin-top: 20px;
}
.input-group input {
  padding: 8px 35px 8px 10px;
  width: 200px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.eye-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.pink-btn {
  margin-top: 20px;
  background: #f56c6c;
  color: #fff;
  border: none;
  padding: 8px 20px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
}
.pink-btn:hover {
  background: #f44336;
}
.links {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.time {
  position: absolute;
  bottom: 50px;
  width: 100%;
  font-size: 24px;
  font-weight: bold;
}

.date {
  position: absolute;
  bottom: 20px;
  width: 100%;
  font-size: 14px;
  color: #666;
}
</style>
