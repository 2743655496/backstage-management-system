import Vue from "vue";
import VueI18n from "vue-i18n";
import enLocale from 'element-ui/lib/locale/lang/en'
import zhLocale from 'element-ui/lib/locale/lang/zh-CN'
import ElementLocale from 'element-ui/lib/locale'

Vue.use(VueI18n)

// 准备翻译的语言环境信息
const messages = {
    //英文
    en: {
        //页面
        menu: {
            home: "Home",
            goods: "Goods Manage",
            params: "Params Manage",
            specification_category: 'Specification'
        },
        ...enLocale,
        //login
        login: {
            label_width: "82px",
            background_content: "My out-of-the-box admin system",
            title: "Welcome Back ✨",
            title_content: "Enter your account details to manage your projects",
            username: "Username:",
            username_placeholder: "Please enter username",
            password: "Password:",
            password_placeholder: "Please enter password",
            SliderVerify_text: "Slider and drag",
            SliderVerify_successText: "Passed",
            remember_me: "Remember Me",
            foget_pwd: "Forgot Password?",
            login_button: "Login",
            mobile_login_button: "Mobile Login",
            qr_code_login_button: "QR Code Login",
            login_else: "OR CONTINUE WITH",
            footer_content_start: "Don't have an account?",
            footer_content_end: "Create Account"
        }

    },
    zh: {
        menu: {
            home: "首页",
            goods: "商品管理",
            params: "参数管理",
            specification_category: '规格类目'
        },
        ...zhLocale,
        //login
        login: {
            label_width: "54px",
            background_content: "我的开箱即用的后台管理系统",
            title: "欢迎回来 ✨",
            title_content: "请输入您的账户信息以开始管理您的项目",
            username: "账号:",
            username_placeholder: "请输入用户名",
            password: "密码:",
            password_placeholder: "请输入密码",
            SliderVerify_text: "拖动滑块完成验证",
            SliderVerify_successText: "验证通过！",
            remember_me: "记住我",
            foget_pwd: "忘记密码?",
            login_button: "登录",
            mobile_login_button: "手机号登录",
            qr_code_login_button: "扫码登录",
            login_else: "其他登录方式",
            footer_content_start: "还没有账号？",
            footer_content_end: "创建账号",
        }
    }
}

//通过选项创建VueI18n实例
const i18n = new VueI18n({
    locale: 'zh',//选中的语言
    messages,//语言环境
})

ElementLocale.i18n((key, value) => i18n.t(key, value))
//导出i18n
export default i18n

