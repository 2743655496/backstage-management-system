<template>
  <div class="menu-page">
    <el-card class="card">
      <div class="header">
        <el-button
          size="medium"
          type="primary"
          icon="el-icon-plus"
          @click="openForm()"
          >新增菜单</el-button
        >
      </div>

      <div class="table-wrapper">
        <el-table
          :data="menuTree"
          :height="tableHeight"
          row-key="id"
          border
          stripe
          :tree-props="{ children: 'children' }"
          :row-class-name="rowClassName"
        >
          <el-table-column prop="name" label="标题" fixed />
          <el-table-column label="图标" width="80" align="center">
            <template slot-scope="scope">
              <i :class="scope.row.icon" />
            </template>
          </el-table-column>
          <el-table-column prop="path" label="访问路径" />
          <el-table-column prop="component" label="页面组件" />
          <el-table-column prop="sort" label="排序" width="80" align="center" />
          <el-table-column
            prop="status"
            label="状态"
            width="100"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
                {{ scope.row.status === 1 ? "启用" : "禁用" }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="visible"
            label="是否显示"
            width="100"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="scope.row.visible === 1 ? 'success' : 'info'">
                {{ scope.row.visible === 1 ? "显示" : "隐藏" }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            width="180"
            align="center"
            fixed="right"
          >
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="addChild(scope.row)"
                >新增下级</el-button
              >
              <el-button
                type="text"
                size="small"
                @click="editRow(scope.row)"
                style="color: #67c23a"
                >编辑</el-button
              >
              <el-button
                type="text"
                size="small"
                @click="deleteRow(scope.row)"
                style="color: red"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>
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
import { getMenus, toDeleteMenu } from "@/api/modules/System/menu";

export default {
  components: { MenuForm },
  data() {
    return {
      tableHeight: 500,
      formVisible: false,
      currentMenu: null,
      menuTree: [],
      resizeTimer: null, // 防抖计时器
    };
  },
  created() {
    this.fetchMenus();
  },
  mounted() {
    this.$nextTick(() => {
      this.updateTableHeight();
      window.addEventListener("resize", this.handleResize);
    });
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
    if (this.resizeTimer) {
      clearTimeout(this.resizeTimer);
    }
  },
  methods: {
    // 防抖的 resize 处理
    handleResize() {
      if (this.resizeTimer) {
        clearTimeout(this.resizeTimer);
      }
      this.resizeTimer = setTimeout(() => {
        this.updateTableHeight();
      }, 150); // 150ms 防抖延迟
    },

    updateTableHeight() {
      const cardEl = this.$el.querySelector(".card");
      const headerEl = cardEl.querySelector(".header");

      if (cardEl && headerEl) {
        const cardHeight = cardEl.clientHeight;
        const headerHeight = headerEl.clientHeight;
        const marginBottom = 10;
        const paddingFix = 40;

        this.tableHeight =
          cardHeight - headerHeight - marginBottom - paddingFix;
      }
    },
    // 其他方法保持不变
    fetchMenus() {
      getMenus()
        .then((res) => {
          this.menuTree = res.data.data;
        })
        .catch(() => {});
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
      })
        .then(() => {
          toDeleteMenu(row.id)
            .then(() => {
              this.$message.success("菜单删除成功");
              this.fetchMenus();
            })
            .catch((err) => {
              this.$message.error(err.response?.data?.error || "菜单删除失败");
            });
        })
        .catch(() => {});
    },
    rowClassName({ row }) {
      return row.type === "按钮" ? "row-button" : "";
    },
  },
};
</script>

<style lang="less" scoped>
.menu-page {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  height: 100%;
  background-color: aqua;
  overflow: hidden;

  .card {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;

    .header {
      display: flex;
      justify-content: flex-end;
      margin-bottom: 10px;
      flex-shrink: 0;
    }

    .table-wrapper {
      flex: 1;
      min-height: 0;
      overflow: auto;

      ::v-deep .el-table {
        width: 100%;
      }

      // ::v-deep .el-table__body-wrapper {
      //   overflow: auto;
      // }

      // ::v-deep .el-table__body-wrapper::-webkit-scrollbar {
      //   width: 8px;
      // }

      // ::v-deep .el-table__body-wrapper::-webkit-scrollbar-thumb {
      //   background-color: #bbb;
      //   border-radius: 4px;
      // }

      // ::v-deep .el-table__body-wrapper::-webkit-scrollbar-track {
      //   background-color: #f5f5f5;
      // }

      // ::v-deep .el-table__body-wrapper::-webkit-scrollbar:horizontal {
      //   height: 8px;
      // }
    }
  }
}
</style>
