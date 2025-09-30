<template>
  <el-drawer
    :title="form.id ? '编辑权限' : '添加权限'"
    :visible="localVisible"
    direction="rtl"
    size="500px"
    :with-header="true"
    append-to-body
    @close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="form" label-width="100px">
      <el-form-item label="上级权限" prop="parent_id">
        <tree-select
          v-model="form.parent_id"
          :data="treeData"
          :disabled="!!form.id"
        />
      </el-form-item>

      <el-form-item label="权限名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入权限名称" />
      </el-form-item>

      <el-form-item label="权限标识" prop="code">
        <el-input v-model="form.code" placeholder="请输入权限标识" />
      </el-form-item>

      <el-form-item label="权限类型" prop="type">
        <el-select v-model="form.type" placeholder="请选择权限类型">
          <el-option :label="'菜单权限'" :value="1" />
          <el-option :label="'接口权限'" :value="2" />
          <el-option :label="'按钮权限'" :value="3" />
        </el-select>
      </el-form-item>

      <el-form-item label="接口方法" prop="api_method" v-if="form.type === 2">
        <el-select v-model="form.api_method" placeholder="请选择接口方法">
          <el-option label="GET" value="GET" />
          <el-option label="POST" value="POST" />
          <el-option label="PUT" value="PUT" />
          <el-option label="DELETE" value="DELETE" />
        </el-select>
      </el-form-item>

      <el-form-item label="接口路径" prop="api_path" v-if="form.type === 2">
        <el-input v-model="form.api_path" placeholder="请输入接口路径" />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio :label="1">启用</el-radio>
          <el-radio :label="2">禁用</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <div class="drawer-footer">
      <el-button @click="handleClose">取消</el-button>
      <el-button @click="resetForm">重置</el-button>
      <el-button type="primary" @click="submitForm">确认</el-button>
    </div>
  </el-drawer>
</template>

<script>
import TreeSelect from "@/components/TreeSelect.vue";
// import { toAddPermission, toUpdatePermission } from "@/api/permission";

export default {
  name: "PermissionForm",
  props: {
    visible: Boolean,
    permission: { type: Object, default: () => ({}) },
    permissions: { type: Array, default: () => [] },
  },
  components: { TreeSelect },
  data() {
    return {
      localVisible: false,
      treeData: [],
      form: {
        name: "",
        code: "",
        type: 1,
        api_method: "",
        api_path: "",
        status: 1,
        parent_id: 0,
      },
      rules: {
        name: [{ required: true, message: "请输入权限名称", trigger: "blur" }],
        code: [{ required: true, message: "请输入权限标识", trigger: "blur" }],
        type: [{ required: true, message: "请选择权限类型", trigger: "change" }],
        api_method: [
          {
            required: true,
            message: "请选择接口方法",
            trigger: "change",
          },
        ],
        api_path: [
          {
            required: true,
            message: "请输入接口路径",
            trigger: "blur",
          },
        ],
        status: [{ required: true, message: "请选择状态", trigger: "change" }],
      },
    };
  },
  watch: {
    visible(val) {
      this.localVisible = val;
    },
    permission: {
      immediate: true,
      handler(val) {
        this.form = val
          ? { ...val }
          : {
              name: "",
              code: "",
              type: 1,
              api_method: "",
              api_path: "",
              status: 1,
              parent_id: 0,
            };
      },
    },
    permissions: {
      immediate: true,
      handler(val) {
        this.treeData = this.transformToTree(val);
      },
    },
  },
  methods: {
    transformToTree(data) {
      return data.map((item) => {
        const newItem = { ...item, label: item.name };
        if (item.children && item.children.length > 0) {
          newItem.children = this.transformToTree(item.children);
        }
        return newItem;
      });
    },
    handleClose() {
      this.$emit("update:visible", false);
    },
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (!valid) return;
        const isEdit = !!this.form.id;
        const payload = { ...this.form };
        if (isEdit) {
          toUpdatePermission(this.form.id, payload)
            .then(() => {
              this.$message.success("权限修改成功");
              this.$emit("refresh");
              this.handleClose();
            })
            .catch((err) => {
              this.$message.error(err.response?.data?.error || "权限修改失败");
            });
        } else {
          toAddPermission(payload)
            .then(() => {
              this.$message.success("添加权限成功");
              this.$emit("refresh");
              this.handleClose();
            })
            .catch((err) => {
              this.$message.error(err.response?.data?.error || "权限添加失败");
            });
        }
      });
    },
    resetForm() {
      if (this.$refs.form) this.$refs.form.resetFields();
      this.form =
        this.permission && this.permission.id
          ? { ...this.permission }
          : {
              name: "",
              code: "",
              type: 1,
              api_method: "",
              api_path: "",
              status: 1,
              parent_id: 0,
            };
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
.el-form-item .el-input-number,
.el-form-item .el-switch,
.el-form-item .el-radio-group,
.el-form-item .tree-select {
  width: 380px;
}
</style>
