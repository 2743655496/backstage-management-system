<template>
  <el-drawer
    :title="menu && menu.id ? '编辑菜单' : '添加菜单'"
    :visible="localVisible"
    direction="rtl"
    size="500px"
    :with-header="true"
    append-to-body
    @close="handleClose"
  >

    <el-form :model="form" :rules="rules" ref="form" label-width="100px" >
      <el-form-item label="上级菜单" prop="name1">
        <tree-select v-model="form.singleValue" :data="treeData" />
      </el-form-item>
      <el-form-item label="菜单名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="菜单图标" prop="icon">
        <el-input v-model="form.icon" />
      </el-form-item>
      <el-form-item label="路由路径" prop="path">
        <el-input v-model="form.path" />
      </el-form-item>
      <el-form-item label="组件路径" prop="component">
        <el-input v-model="form.component" />
      </el-form-item>
      <el-form-item label="菜单排序" prop="sort">
        <el-input-number v-model="form.sort" :min="0" />
      </el-form-item>
      <el-form-item label="是否显示" prop="visible">
        <el-switch v-model="form.visible" />
      </el-form-item>
      <el-form-item label="菜单状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio :label="1">启用</el-radio>
          <el-radio :label="0">禁用</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <div class="drawer-footer">
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="submitForm">确认</el-button>
    </div>
  </el-drawer>
</template>

<script>
import TreeSelect from "@/components/TreeSelect.vue";
export default {
  name: "MenuForm",
  props: {
    visible: Boolean,
    menu: {
      type: Object,
      default: () => ({}),
    },
    menus: {
      type: Array,
      default: () => [],
    },
  },
  components: { TreeSelect },
  data() {
    return {
      treeData: [
      ],
      localVisible: false,
      form: {
        name: "",
        icon: "",
        path: "",
        component: "",
        sort: 0,
        visible: 1,
        status: 1,
        singleValue: null,
      },
      rules: {
        name: [{ required: true, message: "请输入菜单名称", trigger: "blur" }],
      },
    };
  },
  watch: {
    visible(val) {
      this.localVisible = val;
    },
    menu: {
      immediate: true,
      handler(val) {
        this.form = val
          ? {
              name: val.name || "",
              icon: val.icon || "",
              path: val.path || "",
              component: val.component || "",
              sort: val.sort || 0,
              visible: val.visible ?? 1,
              status: val.status ?? 1,
              parent_id: val.parent_id || 0,
            }
          : {
              name: "",
              icon: "",
              path: "",
              component: "",
              sort: 0,
              visible: 1,
              status: 1,
              parent_id: 0,
            };
      },
    },
    menus: {
      immediate: true,
      handler(val) {
        this.treeData = this.transformMenusToTree(val);
      },
    },
  },
  methods: {
    transformMenusToTree(data) {
      return data.map(item => {
        const newItem = {
          ...item,
          label: item.name,
        };
        if (item.children && item.children.length > 0) {
          newItem.children = this.transformMenusToTree(item.children);
        }
        return newItem;
      });
    },
    handleClose() {
      this.$emit("update:visible", false);
    },
    submitForm() {
      console.log(this.form)
      // this.$refs.form.validate((valid) => {
      //   if (!valid) return;
      //   this.$message.success("表单验证通过（模拟保存）");
      //   this.$emit("refresh");
      //   this.handleClose();
      // });
    },
  },
};
</script>

<style scoped>
.drawer-footer {
  position: absolute;   /* 绝对定位 */
  bottom: 0;            /* 贴紧底部 */
  right: 0;             /* 靠右 */
  width: 100%;          /* 占满宽度 */
  padding: 10px 20px;   /* 内边距 */
  text-align: right;    /* 按钮靠右 */
  border-top: 1px solid #eee; /* 顶部分隔线，可选 */
  background: #fff;     /* 背景色，避免和表单混在一起 */
  z-index: 1;
}
.el-form {
  padding-bottom: 60px; /* 留出按钮高度的空间 */
}

/* 统一设置表单控件宽度 */
.el-form-item .el-input,
.el-form-item .el-input-number,
.el-form-item .el-switch,
.el-form-item .el-radio-group,
.el-form-item .tree-select {
  width: 380px;
}
</style>
