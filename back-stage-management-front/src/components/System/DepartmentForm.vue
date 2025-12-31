<template>
  <el-drawer
    :title="form.id ? '编辑部门' : '添加部门'"
    :visible="localVisible"
    direction="rtl"
    size="500px"
    :with-header="true"
    append-to-body
    @close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="form" label-width="100px">
      <el-form-item label="上级部门" prop="parent_id">
        <tree-select
          v-model="form.parent_id"
          :data="treeData"
          :disabled="!!form.id"
        />
      </el-form-item>

      <el-form-item label="部门名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入部门名称" />
      </el-form-item>

      <el-form-item label="部门编码" prop="code">
        <el-input v-model="form.code" placeholder="请输入部门编码" />
      </el-form-item>

      <el-form-item label="部门描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入部门描述"
          style="width: 378.4px"
        />
      </el-form-item>

      <el-form-item label="负责人" prop="manager_id">
        <el-select
          v-model="form.manager_id"
          placeholder="请选择负责人"
          filterable
        >
          <el-option
            v-for="user in userOptions"
            :key="user.id"
            :label="user.real_name || user.username"
            :value="user.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="排序" prop="sort">
        <el-input-number v-model="form.sort" :min="0" />
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
  toAddDepartment,
  toUpdateDepartment,
  getDepartmentPrincipal,
} from "@/api/modules/System/department";

export default {
  name: "DepartmentForm",
  props: {
    visible: Boolean,
    department: { type: Object, default: () => ({}) },
    departments: { type: Array, default: () => [] },
  },
  components: { TreeSelect },
  data() {
    return {
      localVisible: false,
      treeData: [],
      userOptions: [],
      form: {
        name: "",
        code: "",
        description: "",
        parent_id: 0,
        manager_id: null,
        sort: 0,
        status: 1,
      },
      rules: {
        name: [
          { required: true, message: "请输入部门名称", trigger: "blur" },
          { max: 50, message: "部门名称不能超过50个字符", trigger: "blur" },
        ],
        code: [
          { required: true, message: "请输入部门编码", trigger: "blur" },
          { max: 50, message: "部门编码不能超过50个字符", trigger: "blur" },
        ],
        description: [
          { max: 255, message: "部门描述不能超过255个字符", trigger: "blur" },
        ],
        sort: [
          {
            type: "number",
            required: true,
            message: "请输入排序值",
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
      if (val) {
        this.fetchUsers();
        // ✅ 打开弹窗后重置表单验证状态
        this.$nextTick(() => {
          if (this.$refs.form) {
            this.$refs.form.clearValidate();
          }
        });
      }
    },
    department: {
      immediate: true,
      handler(val) {
        this.form = val
          ? { ...val }
          : {
              name: "",
              code: "",
              description: "",
              parent_id: 0,
              manager_id: null,
              sort: 0,
              status: 1,
            };

        // ✅ 当部门数据变化时也清除验证状态
        this.$nextTick(() => {
          if (this.$refs.form) {
            this.$refs.form.clearValidate();
          }
        });
      },
    },
    departments: {
      immediate: true,
      handler(val) {
        this.treeData = this.transformToTree(val);
      },
    },
  },
  methods: {
    fetchUsers() {
      getDepartmentPrincipal()
        .then((res) => {
          this.userOptions = res.data || [];
        })
        .catch((err) => {
          if (!err.__handled) {
            this.$message.error("获取负责人列表失败");
          }
        });
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

        // ✅ 构建干净的提交数据
        const payload = {
          name: this.form.name?.trim(),
          code: this.form.code?.trim(),
          description: this.form.description?.trim(),
          manager_id: this.form.manager_id,
          sort: this.form.sort,
          status: this.form.status,
        };

        // ✅ 新增时才传 parent_id
        if (!isEdit) {
          payload.parent_id = this.form.parent_id;
        }

        const action = isEdit
          ? toUpdateDepartment(this.form.id, payload)
          : toAddDepartment(payload);

        action
          .then(() => {
            this.$message.success(isEdit ? "部门修改成功" : "添加部门成功");
            this.$emit("refresh");
            this.handleClose();
            this.resetForm();
          })
          .catch((err) => {
            if (!err.__handled) {
              this.$message.error(isEdit ? "部门修改失败" : "添加部门失败");
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

      // ✅ 设置表单默认值
      this.form =
        this.department && this.department.id
          ? { ...this.department }
          : {
              name: "",
              code: "",
              description: "",
              parent_id: 0,
              manager_id: null,
              sort: 0,
              status: 1,
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