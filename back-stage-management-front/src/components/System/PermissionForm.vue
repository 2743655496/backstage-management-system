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
          <el-option label="菜单权限" :value="1" />
          <el-option label="接口权限" :value="2" />
          <el-option label="按钮权限" :value="3" />
        </el-select>
      </el-form-item>

      <el-form-item label="权限描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入权限描述"
        />
      </el-form-item>

      <el-form-item label="关联菜单" prop="menu_id" v-if="form.type === 1">
        <tree-select
          v-model="form.menu_id"
          :data="menuOptions"
          :disabled="false"
        />
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
          <el-radio :label="0">禁用</el-radio>
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
import {
  toAddPermission,
  toUpdatePermission,
} from "@/api/modules/System/permission";
import { getMenus } from "@/api/modules/System/menu";

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
      menuOptions: [],
      form: {
        name: "",
        code: "",
        description: "",
        type: 1,
        api_method: "",
        api_path: "",
        status: 1,
        parent_id: 0,
        menu_id: null,
      },
      rules: {
        name: [
          { required: true, message: "请输入权限名称", trigger: "blur" },
          { max: 50, message: "权限名称不能超过50个字符", trigger: "blur" },
        ],
        code: [
          { required: true, message: "请输入权限标识", trigger: "blur" },
          { max: 100, message: "权限标识不能超过100个字符", trigger: "blur" },
          {
            pattern: /^[a-zA-Z0-9:_-]+$/,
            message: "只能包含字母、数字、冒号、下划线、短横线",
            trigger: "blur",
          },
        ],
        type: [
          { required: true, message: "请选择权限类型", trigger: "change" },
        ],
        description: [
          { max: 255, message: "权限描述不能超过255个字符", trigger: "blur" },
        ],
        api_method: [
          {
            validator: (_, value, callback) => {
              if (this.form.type === 2 && !value) {
                callback(new Error("请选择接口方法"));
              } else {
                callback();
              }
            },
            trigger: "change",
          },
        ],
        api_path: [
          {
            validator: (_, value, callback) => {
              if (this.form.type === 2 && !value) {
                callback(new Error("请输入接口路径"));
              } else {
                callback();
              }
            },
            trigger: "blur",
          },
        ],
        menu_id: [
          {
            validator: (_, value, callback) => {
              if (this.form.type === 1 && !value) {
                callback(new Error("请选择关联菜单"));
              } else {
                callback();
              }
            },
            trigger: "change",
          },
        ],
        status: [{ required: true, message: "请选择状态", trigger: "change" }],
      },
    };
  },
  watch: {
    visible(val) {
      this.localVisible = val;
      if (val) {
        this.loadMenus();
        // ✅ 打开弹窗后清除表单验证状态
        this.$nextTick(() => {
          if (this.$refs.form) {
            this.$refs.form.clearValidate();
          }
        });
      }
    },
    permission: {
      immediate: true,
      handler(val) {
        this.form = val
          ? { ...val }
          : {
              name: "",
              code: "",
              description: "",
              type: 1,
              api_method: "",
              api_path: "",
              status: 1,
              parent_id: 0,
              menu_id: null,
            };
        
        // ✅ 当权限数据变化时也清除验证状态
        this.$nextTick(() => {
          if (this.$refs.form) {
            this.$refs.form.clearValidate();
          }
        });
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
    async loadMenus() {
      try {
        const res = await getMenus();
        this.menuOptions = this.transformToTree(res.data.data || []);
      } catch (err) {
        this.$message.error("菜单加载失败");
      }
    },
    transformToTree(data) {
      return data.map((item) => {
        const newItem = { ...item, label: item.name };
        if (item.children?.length) {
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
        const basePayload = {
          name: this.form.name,
          code: this.form.code,
          type: this.form.type,
          description: this.form.description,
          status: this.form.status,
        };

        let payload = { ...basePayload };

        if (!isEdit) {
          payload.parent_id = this.form.parent_id;
        }

        if (this.form.type === 1) {
          payload.menu_id = this.form.menu_id;
        } else if (this.form.type === 2) {
          payload.api_method = this.form.api_method;
          payload.api_path = this.form.api_path;
        }

        const action = isEdit
          ? toUpdatePermission(this.form.id, payload)
          : toAddPermission(payload);

        action
          .then(() => {
            this.$message.success(isEdit ? "权限修改成功" : "添加权限成功");
            this.$emit("refresh");
            this.handleClose();
          })
          .catch((err) => {
            if (!err.__handled) {
              this.$message.error(
                err.response?.data?.error || isEdit
                  ? "权限修改失败"
                  : "添加权限失败"
              );
            }
          });
      });
    },

    resetForm() {
      if (this.$refs.form) {
        // ✅ 先重置表单数据，再清除验证状态
        this.$refs.form.resetFields();
        // ✅ 额外调用 clearValidate 确保验证状态完全清除
        this.$nextTick(() => {
          this.$refs.form.clearValidate();
        });
      }
      
      this.form =
        this.permission && this.permission.id
          ? { ...this.permission }
          : {
              name: "",
              code: "",
              description: "",
              type: 1,
              api_method: "",
              api_path: "",
              status: 1,
              parent_id: 0,
              menu_id: null,
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
.el-form-item .tree-select,
.el-form-item .el-select {
  width: 380px;
}
</style>