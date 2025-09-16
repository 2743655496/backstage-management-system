<template>
  <div class="lock-screen">
    <div class="lock-box">
      <img :src="avatar" class="avatar" />
      <p class="time">{{ currentTime }}</p>
      <p class="date">{{ currentDate }}</p>
      <button class="pink-btn" @click="$emit('unlockClick')">点击解锁</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["avatar"],
  data() {
    return {
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
  },
};
</script>

<style scoped>
.lock-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}
.lock-box {
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
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
.time {
  font-size: 24px;
  margin-top: 15px;
}
.date {
  font-size: 16px;
  color: #666;
}
</style>
