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
    <el-form :model="form" :rules="rules" ref="form" label-width="100px">
      <el-form-item label="上级菜单" prop="parent_id">
        <tree-select
          v-model="form.parent_id"
          :data="treeData"
          :disabled="!!form.id"
        />
      </el-form-item>

      <el-form-item label="菜单名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入菜单名称" />
      </el-form-item>

      <!-- 菜单图标选择 -->
      <el-form-item label="菜单图标" prop="icon">
        <el-input v-model="form.icon" placeholder="请输入或选择图标">
          <template slot="append">
            <el-dropdown trigger="click" @command="selectIcon">
              <el-button
                :icon="form.icon ? form.icon : 'el-icon-s-grid'"
              ></el-button>
              <el-dropdown-menu slot="dropdown" class="icon-dropdown">
                <div class="icon-search">
                  <el-input
                    v-model="iconSearch"
                    placeholder="搜索图标..."
                    clearable
                    size="small"
                    prefix-icon="el-icon-search"
                  />
                </div>
                <div class="icon-grid">
                  <el-dropdown-item
                    v-for="item in pagedIcons"
                    :key="item"
                    :command="item"
                  >
                    <el-tooltip effect="dark" :content="item" placement="top">
                      <div class="icon-item">
                        <i :class="item"></i>
                      </div>
                    </el-tooltip>
                  </el-dropdown-item>
                </div>
                <div class="icon-pagination">
                  <el-pagination
                    layout="prev, pager, next"
                    :page-size="pageSize"
                    :total="filteredIcons.length"
                    :current-page.sync="currentPage"
                    small
                  />
                </div>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="路由路径" prop="path">
        <el-input v-model="form.path" placeholder="请输入路由路径" />
      </el-form-item>

      <el-form-item label="组件路径" prop="component">
        <el-input v-model="form.component" placeholder="请输入组件路径" />
      </el-form-item>

      <el-form-item label="菜单排序" prop="sort">
        <el-input-number v-model="form.sort" :min="0" />
      </el-form-item>

      <el-form-item label="是否显示" prop="visible">
        <el-switch
          v-model="form.visible"
          :active-value="1"
          :inactive-value="0"
        />
      </el-form-item>

      <el-form-item label="菜单状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio :label="1">启用</el-radio>
          <el-radio :label="0">禁用</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- ✅ 新增：是否自动添加权限 -->
      <el-form-item prop="auto_permission" label-width="30px">
        <el-checkbox v-model="form.auto_permission">自动添加权限</el-checkbox>
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
import icons from "@/assets/icons.js";
import { toAddMenu, toUpdateMenu } from "@/api/modules/System/menu";

export default {
  name: "MenuForm",
  props: {
    visible: Boolean,
    menu: { type: Object, default: () => ({}) },
    menus: { type: Array, default: () => [] },
  },
  components: { TreeSelect },
  data() {
    return {
      iconSearch: "",
      iconList: icons,
      currentPage: 1,
      pageSize: 12,
      treeData: [],
      localVisible: false,
      form: {
        name: "",
        icon: "",
        path: "",
        component: "",
        sort: 0,
        visible: 1,
        status: 1,
        parent_id: 0,
        auto_permission: true, // ✅ 新增字段
      },
      rules: {
        name: [
          { required: true, message: "请输入菜单名称", trigger: "blur" },
          {
            min: 1,
            max: 50,
            message: "菜单名称长度在1到50个字符之间",
            trigger: "blur",
          },
        ],
        icon: [
          { max: 50, message: "图标名称不能超过50个字符", trigger: "blur" },
        ],
        path: [
          {
            required: true,
            max: 100,
            message: "路由路径不能超过100个字符",
            trigger: "blur",
          },
          {
            pattern: /^\/[a-zA-Z0-9/_-]*$/,
            message:
              "路由路径必须以 / 开头，只能包含字母、数字、下划线、- 和 /",
            trigger: "blur",
          },
        ],
        component: [
          {
            required: true,
            max: 100,
            message: "组件路径不能超过100个字符",
            trigger: "blur",
          },
          {
            pattern: /^[a-zA-Z0-9/_-]+$/,
            message: "组件路径只能包含字母、数字、下划线、- 和 /",
            trigger: "blur",
          },
        ],
        sort: [
          {
            type: "number",
            required: true,
            message: "请输入排序值",
            trigger: "change",
          },
          {
            type: "number",
            min: 0,
            message: "排序必须为非负整数",
            trigger: "change",
          },
        ],
        visible: [
          {
            type: "number",
            required: true,
            message: "请选择是否显示",
            trigger: "change",
          },
        ],
        status: [
          {
            type: "number",
            required: true,
            message: "请选择菜单状态",
            trigger: "change",
          },
        ],
        auto_permission: [{ type: "boolean", required: false }], // ✅ 可选校验
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
          ? { ...val, auto_permission: val.auto_permission ?? true } // ✅ 回显处理
          : {
              name: "",
              icon: "",
              path: "",
              component: "",
              sort: 0,
              visible: 1,
              status: 1,
              parent_id: 0,
              auto_permission: true, // ✅ 默认值
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
  computed: {
    filteredIcons() {
      if (!this.iconSearch) return this.iconList;
      return this.iconList.filter((icon) =>
        icon.toLowerCase().includes(this.iconSearch.toLowerCase())
      );
    },
    pagedIcons() {
      const start = (this.currentPage - 1) * this.pageSize;
      return this.filteredIcons.slice(start, start + this.pageSize);
    },
  },
  methods: {
    selectIcon(icon) {
      this.form.icon = icon;
    },
    transformMenusToTree(data) {
      return data.map((item) => {
        const newItem = { ...item, label: item.name };
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
      this.$refs.form.validate((valid) => {
        if (!valid) return;
        const payload = {
          name: this.form.name,
          icon: this.form.icon,
          path: this.form.path,
          component: this.form.component,
          sort: this.form.sort,
          status: this.form.status,
          visible: this.form.visible,
        };
        const isEdit = !!this.form.id;
        if (isEdit) {
          toUpdateMenu(this.form.id, payload)
            .then(() => {
              this.$message.success("菜单修改成功");
              this.$emit("refresh");
              this.handleClose();
            })
            .catch((err) => {
              if (!err.__handled) {
                this.$message.error(
                   "菜单修改失败"
                );
              }
            });
        } else {
          toAddMenu({
            ...payload,
            parent_id: this.form.parent_id,
            auto_permission: this.form.auto_permission, // ✅ 关键字段
          })
            .then((res) => {
              this.$message.success("添加菜单成功");
              this.$emit("refresh");
              this.handleClose();
            })
            .catch((err) => {
              if (!err.__handled) {
                this.$message.error(
                  "添加菜单失败"
                );
              }
            });
        }
      });
    },
    resetForm() {
      if (this.$refs.form) this.$refs.form.resetFields();
      this.form =
        this.menu && this.menu.id
          ? {
              ...this.menu,
              auto_permission: this.menu.auto_permission ?? true,
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
              auto_permission: true,
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

/* 去掉 el-dropdown-item 默认的 padding 和对齐 */
.el-dropdown-menu__item {
  padding: 0 !important;
  margin: 0 !important;
  text-align: center !important;
}

.icon-dropdown {
  width: 360px; /* 固定宽度 */
  height: auto; /* 高度由行数决定 */
  padding: 8px;
  box-sizing: border-box;
}

.icon-search {
  margin-bottom: 6px;
  text-align: center;
}

.icon-search .el-input {
  width: 340px;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 一行5列 */
  grid-template-rows: repeat(2, 1fr); /* 固定2行 */
  gap: 8px;
}

.icon-item {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  margin: 0 auto; /* 保证在父容器中居中 */
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}

.icon-item i,
.icon-item .iconfont {
  font-size: 20px;
  line-height: 1;
  margin-left: 5px;
}

.icon-pagination {
  margin-top: 6px;
  text-align: center;
}
</style>
