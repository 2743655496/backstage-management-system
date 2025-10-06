<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-box">
      <!-- 右上角关闭按钮 -->
      <span class="close-btn" @click="close">×</span>

      <img :src="require('@/assets/images/horse.png')" class="avatar" />
      <h3>设定锁屏密码</h3>
      <input type="password" v-model="pwd" placeholder="请输入锁屏密码" />
      <p>
        <button class="pink-btn" @click="confirm">锁定</button>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return { pwd: "" };
  },
  methods: {
    confirm() {
      if (!this.pwd) return this.$message.warning("请输入密码");
      this.$emit("confirm", this.pwd);
    },
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}
.modal-box {
  position: relative;
  width: 300px;
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
.close-btn {
  position: absolute;
  top: 8px;
  right: 12px;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #333;
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}
input {
  margin-top: 15px;
  padding: 8px;
  width: 200px;
  border: 1px solid #ddd;
  border-radius: 4px;
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
</style>
