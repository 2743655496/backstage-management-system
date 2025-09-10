<template>
  <el-container class="loginform">
    <el-header></el-header>
    <el-main>
        手机号登录
    </el-main>
    <el-footer style="height: 30px; font-size: 10px">
      <span>© 2025 the-end-of-the-dream. All rights reserved.</span>
    </el-footer>
  </el-container>
</template>

<script>
import SliderVerify from "@/components/Login/SliderVerify.vue";
export default {
  components: {
    SliderVerify,
  },
  data() {
    return {
      form: {
        captcha: false,
        username: "",
        password: "",
      },
    };
  },
  methods: {
    handleVerifySuccess() {
      console.log("验证通过！");
      // 可执行登录、提交等操作
    },
  },
};
</script>

<style lang="less" scoped>
.loginform {
  height: 100%;
  .el-header {
    text-align: center;
    line-height: 60px;
  }
  .el-footer {
    color: #909399;
    text-align: center;
    line-height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .el-main {
    display: flex;
    justify-content: center;
  }
}
</style>