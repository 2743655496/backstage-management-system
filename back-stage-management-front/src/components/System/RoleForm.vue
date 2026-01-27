<template>
  <el-drawer
    :title="form.id ? '编辑角色' : '新增角色'"
    :visible.sync="visible"
    direction="rtl"
    size="500px"
    :with-header="true"
    append-to-body
    @close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item label="角色名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入角色名称" />
      </el-form-item>

      <el-form-item label="角色编码" prop="code">
        <el-input v-model="form.code" placeholder="请输入角色编码" />
      </el-form-item>

      <el-form-item label="角色描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入角色描述"
        />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio :label="1">启用</el-radio>
          <el-radio :label="0">禁用</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="授权">
        <div class="permission-box">
          <el-tree
            ref="treeRef"
            :data="permissionTree"
            show-checkbox
            node-key="id"
            default-expand-all
            :props="treeProps"
            :default-checked-keys="permissions"
            @check="handlePermissionCheck"
          />
        </div>
      </el-form-item>
    </el-form>

    <div class="drawer-footer">
      <el-button @click="handleClose">取消</el-button>
      <el-button @click="resetForm">重置</el-button>
      <el-button type="primary" @click="submitForm" :loading="loading">
        确认
      </el-button>
    </div>
  </el-drawer>
</template>

<script>
import { getPermissions } from "@/api/modules/System/permission";
import {
  toAddRole,
  toUpdateRole,
  toGetRoleDetail,
} from "@/api/modules/System/role";

export default {
  name: "RoleForm",
  props: {
    visible: Boolean,
    roleId: { type: [Number, String], default: null },
  },
  data() {
    return {
      form: {
        name: "",
        code: "",
        description: "",
        status: 1,
        permissions: [],
      },
      permissions: [],
      permissionTree: [],
      treeProps: {
        children: "children",
        label: "label",
      },
      loading: false,
      rules: {
        name: [
          { required: true, message: "请输入角色名称", trigger: "blur" },
          { max: 50, message: "角色名称不能超过50个字符", trigger: "blur" },
        ],
        code: [
          { required: true, message: "请输入角色编码", trigger: "blur" },
          { max: 50, message: "角色编码不能超过50个字符", trigger: "blur" },
        ],
        description: [
          { max: 255, message: "角色描述不能超过255个字符", trigger: "blur" },
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
          this.$nextTick(() => {
            this.$refs.formRef?.clearValidate();
          });
          this.loadData(); // ⭐ 只在这里加载一次
        } else {
          if (this.form.id) {
            this.resetForm();
          }
        }
      },
    },
  },

  methods: {
    async loadData() {
      this.loading = true;
      try {
        await Promise.all([
          this.loadPermissions(),
          this.roleId ? this.loadRoleDetail() : Promise.resolve(),
        ]);
      } finally {
        this.loading = false;
      }
    },

    async loadPermissions() {
      const res = await getPermissions();
      const raw = res.data?.data || [];
      this.permissionTree = this.transformPermissions(raw);
    },

    async loadRoleDetail() {
      const res = await toGetRoleDetail(this.roleId);
      if (res.data && res.data.success) {
        const roleData = res.data.data;
        this.form = {
          id: roleData.id,
          name: roleData.name || "",
          code: roleData.code || "",
          description: roleData.description || "",
          status: roleData.status || 1,
          permissions: Array.isArray(roleData.permissions)
            ? roleData.permissions
            : [],
        };

        this.permissions = this.extractLeafPermissionIds(
          this.permissionTree,
          this.form.permissions
        );

        this.$nextTick(() => {
          this.setTreeCheckedKeys();
        });
      }
    },

    extractLeafPermissionIds(tree, selectedIds) {
      const leafIds = [];
      const traverse = (nodes) => {
        for (const node of nodes) {
          const hasChildren =
            Array.isArray(node.children) && node.children.length > 0;
          if (!hasChildren && selectedIds.includes(node.id)) {
            leafIds.push(node.id);
          }
          if (hasChildren) {
            traverse(node.children);
          }
        }
      };
      traverse(tree);
      return leafIds;
    },

    setTreeCheckedKeys() {
      this.$refs.treeRef?.setCheckedKeys(this.permissions);
    },

    transformPermissions(list) {
      return list
        .filter((item) => item.status === 1)
        .map((item) => ({
          id: item.id,
          label: item.name,
          children: Array.isArray(item.children)
            ? this.transformPermissions(item.children)
            : [],
        }));
    },

    handlePermissionCheck(checkedNode, checkedInfo) {
      this.permissions = checkedInfo.checkedKeys || [];
    },

    handleClose() {
      this.$emit("update:visible", false);
    },

    resetForm() {
      this.$refs.formRef?.resetFields();
      this.$nextTick(() => {
        this.$refs.formRef?.clearValidate();
      });

      this.form = {
        name: "",
        code: "",
        description: "",
        status: 1,
        permissions: [],
      };
      this.permissions = [];

      this.$nextTick(() => {
        this.setTreeCheckedKeys();
      });
    },

    async submitForm() {
      this.loading = true;
      try {
        const valid = await this.$refs.formRef.validate();
        if (!valid) return;

        let checkedKeys = [];
        let halfCheckedKeys = [];
        if (this.$refs.treeRef) {
          checkedKeys = this.$refs.treeRef.getCheckedKeys();
          halfCheckedKeys = this.$refs.treeRef.getHalfCheckedKeys();
        }

        const permissionIds = [...checkedKeys, ...halfCheckedKeys];
        const isEdit = !!this.form.id;

        const payload = {
          name: this.form.name,
          code: this.form.code,
          description: this.form.description,
          status: this.form.status,
          permissions: permissionIds,
        };

        if (isEdit) {
          payload.action = "update";
          await toUpdateRole(this.form.id, payload);
        } else {
          await toAddRole(payload);
        }

        this.$message.success(isEdit ? "角色修改成功" : "角色添加成功");
        this.$emit("refresh");
        this.handleClose();
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
.el-form-item .el-radio-group {
  width: 380px;
}
.permission-box {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #fafafa;
  width: 378.4px;
  max-height: 400px;
  overflow-y: auto;
}
</style>
