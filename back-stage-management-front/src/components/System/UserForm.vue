<template>
  <el-drawer
    :title="form.id ? '编辑用户' : '新增用户'"
    :visible.sync="visible"
    direction="rtl"
    size="500px"
    :with-header="true"
    append-to-body
    @close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <!-- 头像上传 -->
      <el-form-item label="头像">
        <div class="avatar-upload-container">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="handleAvatarUpload"
            accept=".jpg,.jpeg,.png,.gif"
          >
            <div class="avatar-uploader-content">
              <img v-if="form.avatar" :src="form.avatar" class="avatar" />
              <div v-else class="avatar-uploader-icon">
                <i class="el-icon-plus avatar-icon"></i>
                <div class="upload-text">点击上传</div>
              </div>
            </div>
          </el-upload>
          <el-button
            type="primary"
            size="small"
            @click="generateRandomAvatar"
            class="random-btn"
          >
            随机头像
          </el-button>
        </div>
      </el-form-item>

      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名" />
      </el-form-item>

      <el-form-item v-if="!form.id" label="密码" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
          show-password
        />
      </el-form-item>

      <el-form-item label="真实姓名" prop="real_name">
        <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮箱" />
      </el-form-item>

      <el-form-item label="手机号" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入手机号" />
      </el-form-item>

      <!-- 使用 TreeSelect 组件 -->
      <el-form-item label="所属部门" prop="department_id">
        <div class="permission-box">
          <TreeSelect
            v-model="form.department_id"
            :data="departmentTree"
            placeholder="请选择部门"
            :multiple="false"
          />
        </div>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio :label="1">启用</el-radio>
          <el-radio :label="0">禁用</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="角色分配">
        <el-select
          v-model="form.role_ids"
          multiple
          filterable
          placeholder="请选择角色"
          style="width: 378.4px"
        >
          <el-option
            v-for="role in roleList"
            :key="role.id"
            :label="role.name"
            :value="role.id"
          >
            <div style="display: flex; align-items: center">
              <span>{{ role.name }}</span>
            </div>
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <div class="drawer-footer">
      <el-button @click="handleClose">取消</el-button>
      <el-button @click="resetForm">重置</el-button>
      <el-button type="primary" @click="submitForm" :loading="loading"
        >确认</el-button
      >
    </div>
  </el-drawer>
</template>

<script>
import { getDepartments } from "@/api/modules/System/department";
import { getRoles } from "@/api/modules/System/role";
import {
  toAddUser,
  toUpdateUser,
  toGetUserDetail,
} from "@/api/modules/System/user";
import TreeSelect from "@/components/TreeSelect.vue";

export default {
  name: "UserForm",
  components: {
    TreeSelect,
  },
  props: {
    visible: Boolean,
    userId: { type: [Number, String], default: null },
  },
  data() {
    // 密码验证函数
    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入密码"));
        return;
      }

      // 检查首字符是否为字母
      if (!/^[a-zA-Z]/.test(value)) {
        callback(new Error("密码首字符必须为字母"));
        return;
      }

      // 检查是否包含数字
      if (!/\d/.test(value)) {
        callback(new Error("密码必须包含至少一个数字"));
        return;
      }

      // 检查是否包含字母
      if (!/[a-zA-Z]/.test(value)) {
        callback(new Error("密码必须包含至少一个字母"));
        return;
      }

      // 检查是否包含特殊字符
      if (!/[!@#$%^&*]/.test(value)) {
        callback(new Error("密码必须包含至少一个特殊字符 (!@#$%^&*)"));
        return;
      }

      // 检查最小长度
      if (value.length < 6) {
        callback(new Error("密码长度不能少于6个字符"));
        return;
      }

      callback();
    };
    return {
      form: {
        username: "",
        password: "",
        real_name: "",
        email: "",
        phone: "",
        department_id: null,
        status: 1,
        role_ids: [],
        avatar: "",
      },
      departmentTree: [], // 直接使用树形数据
      roleList: [],
      loading: false,
      randomAvatars: [
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fww2.sinaimg.cn%2Fmw690%2F0069ziSmly1hy8uhatakkj30sg0sggo5.jpg&thumburl=https%3A%2F%2Fimg0.baidu.com%2Fit%2Fu%3D2424897188%2C89842895%26fm%3D253%26fmt%3Dauto%26app%3D120%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fq7.itc.cn%2Fq_70%2Fimages03%2F20240512%2F8d063c75d60d4c9eb88e1956be2d873d.jpeg&thumburl=https%3A%2F%2Fimg1.baidu.com%2Fit%2Fu%3D2109052374%2C604822922%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fgips1.baidu.com%2Fit%2Fu%3D3834598948%2C2418503949%26fm%3D3074%26app%3D3074%26f%3DPNG%3Fw%3D2048%26h%3D2048&thumburl=https%3A%2F%2Fimg2.baidu.com%2Fit%2Fu%3D1781167939%2C4113493204%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fgips2.baidu.com%2Fit%2Fu%3D2786175775%2C3350769033%26fm%3D3074%26app%3D3074%26f%3DPNG%3Fw%3D2048%26h%3D2048&thumburl=https%3A%2F%2Fimg1.baidu.com%2Fit%2Fu%3D1999384104%2C253229540%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fgips2.baidu.com%2Fit%2Fu%3D1294304757%2C2284873529%26fm%3D3074%26app%3D3074%26f%3DPNG%3Fw%3D2048%26h%3D2048&thumburl=https%3A%2F%2Fimg0.baidu.com%2Fit%2Fu%3D114560984%2C2684912278%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fgips2.baidu.com%2Fit%2Fu%3D1294304757%2C2284873529%26fm%3D3074%26app%3D3074%26f%3DPNG%3Fw%3D2048%26h%3D2048&thumburl=https%3A%2F%2Fimg0.baidu.com%2Fit%2Fu%3D114560984%2C2684912278%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fn.sinaimg.cn%2Fsinakd20115%2F448%2Fw1024h1024%2F20240505%2Ff666-95c7f86ffcf274cdc68f4b646e52cec3.jpg&thumburl=https%3A%2F%2Fimg0.baidu.com%2Fit%2Fu%3D2201786265%2C1996910509%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fww1.sinaimg.cn%2Fmw690%2F00854yfugy1hs8i93ltofj30j60j6dgx.jpg&thumburl=https%3A%2F%2Fimg1.baidu.com%2Fit%2Fu%3D1296132577%2C3216763945%26fm%3D253%26fmt%3Dauto%26app%3D120%26f%3DJPEG%3Fw%3D500%26h%3D500",
        "https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=https%3A%2F%2Fc-ssl.dtstatic.com%2Fuploads%2Fblog%2F202203%2F05%2F20220305205735_f6563.thumb.400_0.jpeg&thumburl=https%3A%2F%2Fimg0.baidu.com%2Fit%2Fu%3D1056874060%2C3663579464%26fm%3D253%26fmt%3Dauto%26app%3D138%26f%3DJPEG%3Fw%3D400%26h%3D400",
      ],
      passwordValid: {
        firstLetter: false,
        hasNumber: false,
        hasLetter: false,
        hasSpecialChar: false,
        minLength: false,
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 3,
            max: 50,
            message: "用户名长度为3-50个字符",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { validator: validatePassword, trigger: "blur" },
        ],
        real_name: [
          { max: 50, message: "真实姓名不能超过50个字符", trigger: "blur" },
        ],
        email: [
          { type: "email", message: "请输入正确的邮箱地址", trigger: "blur" },
        ],
        phone: [
          {
            pattern: /^1[3-9]\d{9}$/,
            message: "请输入正确的手机号码",
            trigger: "blur",
          },
        ],
        status: [{ required: true, message: "请选择状态", trigger: "change" }],
      },
    };
  },
  watch: {
    visible: {
      immediate: true,
      handler(val) {
        if (val) {
          // ✅ 打开弹窗后清除表单验证状态
          this.$nextTick(() => {
            if (this.$refs.formRef) {
              this.$refs.formRef.clearValidate();
            }
          });
          this.loadData();
        } else {
          if(this.form.id){
            this.resetForm();
          }
        }
      },
    },
    userId: {
      immediate: true,
      handler(val) {
        if (val && this.visible) {
          this.loadUserDetail();
        }
      },
    },
  },
  methods: {
    async loadData() {
      try {
        this.loading = true;
        await Promise.all([
          this.loadDepartments(),
          this.loadRoles(),
          this.userId ? this.loadUserDetail() : Promise.resolve(),
        ]);
      } catch (error) {
        console.error("加载数据失败:", error);
        this.$message.error("加载数据失败");
      } finally {
        this.loading = false;
      }
    },

    // 加载部门数据 - 直接使用返回的树形结构
    async loadDepartments() {
      try {
        const res = await getDepartments();
        // 根据您的数据结构，直接使用返回的数据
        this.departmentTree = res.data?.data || [];
        console.log("部门树形数据:", this.departmentTree);
      } catch (error) {
        console.error("加载部门列表失败:", error);
        throw error;
      }
    },

    // 加载角色列表
    async loadRoles() {
      try {
        const res = await getRoles();
        this.roleList = res.data?.data?.results || [];
      } catch (error) {
        console.error("加载角色列表失败:", error);
        throw error;
      }
    },

    // 加载用户详情
    async loadUserDetail() {
      try {
        const res = await toGetUserDetail(this.userId);
        if (res.data && res.data.success) {
          const userData = res.data.data;
          this.form = {
            id: userData.id,
            username: userData.username || "",
            password: "",
            real_name: userData.real_name || "",
            email: userData.email || "",
            phone: userData.phone || "",
            department_id: userData.department_id || null,
            status: userData.status || 1,
            role_ids: Array.isArray(userData.roles)
              ? userData.roles.map((role) => role.id)
              : [],
            avatar: userData.avatar || "",
          };
          console.log("加载用户详情，部门ID:", this.form.department_id);
        }
      } catch (error) {
        console.error("加载用户详情失败:", error);
        throw error;
      }
    },

    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isPNG = file.type === "image/png";
      const isGIF = file.type === "image/gif";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG && !isPNG && !isGIF) {
        this.$message.error("头像只能是 JPG、PNG 或 GIF 格式!");
        return false;
      }
      if (!isLt2M) {
        this.$message.error("头像大小不能超过 2MB!");
        return false;
      }
      return true;
    },

    handleAvatarUpload(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.form.avatar = e.target.result;
          this.$message.success("头像上传成功");
          resolve();
        };
        reader.onerror = reject;
        reader.readAsDataURL(file.file);
      });
    },

    generateRandomAvatar() {
      const randomIndex = Math.floor(Math.random() * this.randomAvatars.length);
      this.form.avatar = this.randomAvatars[randomIndex];
      this.$message.success("已生成随机头像");
    },

    handleClose() {
      this.$emit("update:visible", false);
    },

    resetForm() {
      if (this.$refs.formRef) {
        // ✅ 先重置表单数据，再清除验证状态
        this.$refs.formRef.resetFields();
        // ✅ 额外调用 clearValidate 确保验证状态完全清除
        this.$nextTick(() => {
          this.$refs.formRef.clearValidate();
        });
      }
      this.form = {
        username: "",
        password: "",
        real_name: "",
        email: "",
        phone: "",
        department_id: null,
        status: 1,
        role_ids: [],
        avatar: "",
      };
    },

    async submitForm() {
      try {
        this.loading = true;
        const valid = await this.$refs.formRef.validate();
        if (!valid) return;

        const isEdit = !!this.form.id;
        const payload = { ...this.form };

        if (isEdit && !payload.password) {
          delete payload.password;
          delete payload.id;
        }

        if (isEdit) {
          payload.action = "update";
          await toUpdateUser(this.form.id, payload);
        } else {
          await toAddUser(payload);
        }

        this.$message.success(isEdit ? "用户修改成功" : "用户添加成功");
        this.$emit("refresh");
        this.handleClose();
      } catch (error) {
        if (!error.__handled) {
          const isEdit = !!this.form.id;
          const msg =
            error.response?.data?.error || error.message || isEdit
              ? "用户修改失败"
              : "用户添加失败";
          this.$message.error(msg);
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.drawer-footer {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100%;
  padding: 10px 20px;
  text-align: right;
  border-top: 1px solid #eee;
  background: #fff;
  z-index: 1;
}
.el-form {
  padding-bottom: 60px;
}
.el-form-item .el-input,
.el-form-item .el-textarea,
.el-form-item .el-radio-group,
.el-form-item .el-select {
  width: 380px;
}

.avatar-upload-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-uploader-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.avatar-icon {
  font-size: 24px;
  color: #8c939d;
  margin-bottom: 4px;
}

.upload-text {
  font-size: 12px;
  color: #8c939d;
  text-align: center;
}

.avatar {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.random-btn {
  margin-top: 10px;
  height: 32px;
  white-space: nowrap;
}

:deep(.el-upload) {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 100%;
  border: none;
}
.permission-box {
  border-radius: 4px;
  width: 378.4px;
  max-height: 400px;
}
</style>