<template>
  <el-container class="loginform" :style="background_color_style">
    <el-header></el-header>
    <el-main>
      <div class="form">
        <h1
          style="
            font-family: 'Georgia', serif;
            font-size: 32px;

            font-style: italic;
          "
        >
          {{ $t("login.title") }}
        </h1>
        <p style="color: #909399; font-size: 16px; margin-top: 6px">
          {{ $t("login.title_content") }}
        </p>
        <el-form
          ref="loginForm"
          :rules="rules"
          :model="form"
          :label-width="$t('login.label_width')"
          class="login_form"
          :class="isLightOn ? 'light-mode' : 'dark-mode'"
        >
          <el-form-item :label="$t('login.username')" prop="username">
            <el-input
              v-model="form.username"
              :placeholder="$t('login.username_placeholder')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('login.password')" prop="password">
            <el-input
              v-model="form.password"
              :placeholder="$t('login.password_placeholder')"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item prop="sliderprop" :label-width="'0px'">
            <SliderVerify
              ref="slider"
              @pass="handleVerifySuccess"
              :text="$t('login.SliderVerify_text')"
              :successText="$t('login.SliderVerify_successText')"
            />
          </el-form-item>
        </el-form>

        <div class="remember_me">
          <div class="remember_me_left">
            <el-checkbox
              v-model="form.remember"
              :class="isLightOn ? 'light-mode' : 'dark-mode'"
              >{{ $t("login.remember_me") }}</el-checkbox
            >
          </div>
          <div class="remember_me_right">
            <el-link
              :underline="false"
              type="primary"
              @click="router_path('/auth/forget')"
              >{{ $t("login.foget_pwd") }}</el-link
            >
          </div>
        </div>
        <el-button
          type="primary"
          round
          class="loginbutton"
          @click="handleLogin"
          >{{ $t("login.login_button") }}</el-button
        >
        <el-row :gutter="20" class="loginbuttonelse">
          <el-col :span="12"
            ><div class="grid-content bg-purple">
              <el-button plain @click="router_path('/auth/mobile_login')">{{
                $t("login.mobile_login_button")
              }}</el-button>
            </div></el-col
          >
          <el-col :span="12"
            ><div class="grid-content bg-purple">
              <el-button plain @click="router_path('/auth/qr_code')">{{
                $t("login.qr_code_login_button")
              }}</el-button>
            </div></el-col
          >
        </el-row>
        <div :class="isLightOn ? 'divider-light-mode' : 'divider-dark-mode'">
          <el-divider content-position="center">{{
            $t("login.login_else")
          }}</el-divider>
        </div>

        <div class="social-login-container">
          <!-- Ghost 纯图标无边框按钮 -->
          <button :class="['social-btn', isLightOn ? 'ghost' : 'ghost2']">
            <i class="iconfont icon-github-fill"></i>
          </button>
          <button :class="['social-btn', isLightOn ? 'ghost' : 'ghost2']">
            <i class="iconfont icon-weixin"></i>
          </button>
          <button :class="['social-btn', isLightOn ? 'ghost' : 'ghost2']">
            <i class="iconfont icon-QQ"></i>
          </button>
          <button :class="['social-btn', isLightOn ? 'ghost' : 'ghost2']">
            <i class="iconfont icon-weibo"></i>
          </button>
        </div>
        <el-row class="footer_content">
          <span
            >{{ $t("login.footer_content_start")
            }}<el-link :underline="false" type="primary" class="minimal-link" @click="router_path('/auth/create')">{{
              $t("login.footer_content_end")
            }}</el-link></span
          >
        </el-row>
      </div>
    </el-main>
    <el-footer style="height: 30px; font-size: 10px">
      <span>© 2025 the-end-of-the-dream. All rights reserved.</span>
    </el-footer>
  </el-container>
</template>

<script>
import SliderVerify from "@/components/Login/SliderVerify.vue";
import { toslider_verify } from "@/api/modules/login.js";
import { mapGetters } from "vuex";
export default {
  components: {
    SliderVerify,
  },
  computed: {
    ...mapGetters("LightModule", ["isLightOn"]),
    background_color_style() {
      // 根据 isLightOn 动态计算颜色
      return {
        backgroundColor: this.isLightOn ? "#000000" : "white",
        color: this.isLightOn ? "white" : "black",
      };
    },
  },
  data() {
    return {
      isPassed: false,
      form: {
        remember: false,
        username: "",
        password: "",
        sliderToken: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { min: 4, max: 20, message: "用户名长度为4-20位", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/,
            message: "密码必须包含字母和数字，至少8位",
            trigger: "blur",
          },
        ],
        sliderprop: [
          {
            validator: (rule, value, callback) => {
              if (this.isPassed) {
                callback();
              } else {
                callback(new Error("请完成滑块验证"));
              }
            },
            trigger: "change",
          },
        ],
      },
    };
  },
  methods: {
    //登录
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          if (!this.isPassed || !this.form.sliderToken) {
            this.$message.error("请先完成滑块验证");
            return;
          }

          const loginData = {
            username: this.form.username,
            password: this.form.password,
            slider_token: this.form.sliderToken,
            remember: this.form.remember,
          };

          this.$store
            .dispatch("LoginModule/login", {
              loginData,
              router: this.$router,
              message: this.$message,
            })
            .catch(() => {
              this.$refs.slider?.resetSlider();
              this.form.sliderToken = "";
            });
        }
      });
    },
    //滑块验证
    handleVerifySuccess(trail) {
      toslider_verify({ trail: trail })
        .then((res) => {
          if (res.status === 200 && res.data.success) {
            this.form.sliderToken = res.data.token;
            this.$message.success("滑块验证通过");
            this.isPassed = true;
            this.$refs.loginForm.clearValidate("sliderprop"); // 清除错误提示
          } else {
            this.$message.error("滑块验证失败");
            this.$refs.slider.resetSlider(); // 👈 还原滑块状态
            this.isPassed = false;
          }
        })
        .catch((err) => {
          if (!err.__handled) {
            this.$message.error(err.response?.data?.error || "滑块验证异常");
          }
          this.$refs.slider.resetSlider(); // 👈 还原滑块状态
          this.isPassed = false;
        });
    },
    //路由跳转
    router_path(path) {
      this.$router.push(path);
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
    .form {
      width: 450px;
      .login_form {
        margin-top: 25px;
      }
      .login_form.light-mode {
        ::v-deep(.el-form-item__label) {
          color: white; // 白色
        }
      }

      .login_form.dark-mode {
        ::v-deep(.el-form-item__label) {
          color: #303133; // 原色
        }
      }

      .remember_me {
        display: flex;
        justify-content: space-between;
        align-items: center;
        .remember_me_left {
          .light-mode {
            ::v-deep(.el-checkbox__label) {
              color: #ffffff; // 白色
            }
          }

          .dark-mode {
            ::v-deep(.el-checkbox__label) {
              color: #303133; // 原色
            }
          }
        }
      }
      .loginbutton {
        margin-top: 25px;
        width: 100%;
        max-width: 450px;
      }
      .loginbuttonelse {
        margin-top: 20px;
        .el-button {
          width: 100%;
          max-width: 215.4px;
        }
      }
      .divider-light-mode .el-divider__text {
        position: absolute;
        padding: 0 10px;
        font-weight: 500;
        color: #909399;
        font-size: 13px;
        background-color: #000000;
      }
      .divider-dark-mode .el-divider__text {
        position: absolute;
        padding: 0 10px;
        font-weight: 500;
        color: #909399;
        font-size: 13px;
      }

      .social-login-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        align-items: center;
      }
      /* 公共样式——圆形、居中、交互 */
      .social-btn {
        width: 20px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
      }
      /* Ghost：仅图标，无背景无边框 */
      .social-btn.ghost2 {
        background: transparent;
        border: none;
        color: #303133;
      }
      .social-btn.ghost {
        background: transparent;
        border: none;
        color: white;
      }
      .social-btn.ghost:hover {
        color: #409eff;
      }
      .social-btn.ghost2:hover {
        color: #409eff;
      }
      .footer_content {
        margin-top: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        .minimal-link {
          font-size: 15px;
          margin-top: -2px;

        }
      }
    }
  }
}
</style>