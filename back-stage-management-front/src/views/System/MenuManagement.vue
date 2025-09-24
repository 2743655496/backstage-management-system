<template>
  <div class="menu-page">
    <el-card class="card">
      <div class="header">
        <el-button type="primary" icon="el-icon-plus" @click="openForm()">新增菜单</el-button>
      </div>

      <el-table
        :data="menuTree"
        row-key="id"
        height="500"
        border
        stripe
        :tree-props="{ children: 'children' }"
        :row-class-name="rowClassName"
      >
        <el-table-column prop="name" label="标题" />
        <el-table-column label="图标" width="80" align="center">
          <template slot-scope="scope">
            <i :class="scope.row.icon" />
          </template>
        </el-table-column>
        <el-table-column prop="path" label="访问路径" />
        <el-table-column prop="component" label="页面组件" />
        <el-table-column prop="sort" label="排序" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
              {{ scope.row.status === 1 ? "已启用" : "未启用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="addChild(scope.row)">新增下级</el-button>
            <el-button type="text" size="small" @click="editRow(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteRow(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <menu-form
      :visible.sync="formVisible"
      :menu="currentMenu"
      :menus="menuTree"
      @refresh="fetchMenus"
    />
  </div>
</template>

<script>
import MenuForm from "@/components/System/MenuForm.vue";
import { getMenus } from "@/api/menu";

export default {
  components: { MenuForm },
  data() {
    return {
      formVisible: false,
      currentMenu: null,
      menuTree: [],
    };
  },
  created() {
    this.fetchMenus();
  },
  methods: {
    fetchMenus() {
      getMenus().then((res) => {
        this.menuTree = res.data.data;
      });
    },
    openForm(row = null) {
      this.currentMenu = row ? { ...row } : null;
      this.formVisible = true;
    },
    addChild(parentRow) {
      this.currentMenu = {
        parent_id: parentRow.id,
        name: "",
        icon: "",
        path: "",
        component: "",
        sort: 0,
        visible: 1,
        status: 1,
      };
      this.formVisible = true;
    },
    editRow(row) {
      this.currentMenu = { ...row };
      this.formVisible = true;
    },
    deleteRow(row) {
      this.$confirm(`确定删除 ${row.name} 吗？`, "提示", {
        type: "warning",
      }).then(() => {
        this.$message.success("删除成功（模拟）");
      });
    },
    rowClassName({ row }) {
      return row.type === "按钮" ? "row-button" : "";
    },
  },
};
</script>


<style lang="less" scoped>
.menu-page {
  height: 93.7380104%;
  margin-top: 20px;
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
  background-color: aqua;
  display: flex;
  flex-direction: column;

  .card {
    flex: 1;
    display: flex;
    flex-direction: column;
    .header {
      display: flex;
      justify-content: flex-end;
      margin-bottom: 10px;
    }

    .el-table {
      flex: 1;
      overflow: auto;
    }

    ::v-deep .el-table__body-wrapper::-webkit-scrollbar {
      width: 8px;
    }

    ::v-deep .el-table__body-wrapper::-webkit-scrollbar-thumb {
      background-color: #bbb;
      border-radius: 4px;
    }

    ::v-deep .el-table__body-wrapper::-webkit-scrollbar-track {
      background-color: #f5f5f5;
    }
    ::v-deep .el-table__body-wrapper::-webkit-scrollbar:horizontal {
      height: 8px;
    }
  }
}
</style>
