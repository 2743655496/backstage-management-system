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
        <TreeSelect
          v-model="form.department_id"
          :data="departmentTree"
          placeholder="请选择部门"
          :multiple="false"
        />
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
    TreeSelect
  },
  props: {
    visible: Boolean,
    userId: { type: [Number, String], default: null },
  },
  data() {
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
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Milo",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Oscar",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Charlie",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Max",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Bella",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Lucy",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Bailey",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Luna",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Rocky",
        "https://api.dicebear.com/7.x/avataaars/svg?seed=Zoe",
      ],
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
          { min: 6, message: "密码长度不能少于6个字符", trigger: "blur" },
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
          this.loadData();
        } else {
          this.resetForm();
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
        console.log('部门树形数据:', this.departmentTree);
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
          console.log('加载用户详情，部门ID:', this.form.department_id);
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
        this.$refs.formRef.resetFields();
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
        }

        console.log("提交的数据:", payload);

        if (isEdit) {
          await toUpdateUser(this.form.id, payload);
        } else {
          await toAddUser(payload);
        }

        this.$message.success(isEdit ? "用户修改成功" : "用户添加成功");
        this.$emit("refresh");
        this.handleClose();
      } catch (error) {
        console.error("提交失败:", error);
        const msg = error.response?.data?.error || error.message || "操作失败";
        this.$message.error(msg);
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
</style>