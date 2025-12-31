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
          :tree-props="{ children: 'children' }"
          @cell-mouse-enter="onCellEnter"
          @cell-mouse-leave="onCellLeave"
          :row-class-name="rowClassName"
        >
          <!-- 左侧固定列 -->
          <el-table-column 
            prop="name" 
            label="标题" 
            width="180" 
            fixed="left" 
          />
          
          <!-- 中间普通列 -->
          <el-table-column label="图标" width="80" align="center">
            <template slot-scope="scope">
              <i :class="scope.row.icon" />
            </template>
          </el-table-column>
          <el-table-column prop="path" label="访问路径" width="200" />
          <el-table-column prop="component" label="页面组件" width="200" />
          <el-table-column prop="sort" label="排序" width="80" align="center" />
          <el-table-column
            prop="status"
            label="状态"
            width="100"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
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
              <el-tag :type="scope.row.visible === 1 ? 'success' : 'danger'">
                {{ scope.row.visible === 1 ? "显示" : "隐藏" }}
              </el-tag>
            </template>
          </el-table-column>

          <!-- 右侧固定列 -->
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
import { mapGetters } from "vuex";

export default {
  components: { MenuForm },
  
  computed: {
    ...mapGetters("LightModule", [
      "subBackgroundColor",
      "tableBackgroundColor",
      "tableTextColor",
      "tableHeaderBackgroundColor",
      "tableHeaderTextColor",
      "tableRowHoverBackgroundColor",
    ]),
  },

  data() {
    return {
      tableHeight: 500,
      formVisible: false,
      currentMenu: null,
      menuTree: [],
      resizeTimer: null,
      
      // ⭐ 记录 hover 行
      hoverRowId: null,
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
    if (this.resizeTimer) clearTimeout(this.resizeTimer);
  },
  
  methods: {
    /* -------------------------
     *  ⭐ Hover 行同步逻辑
     * ------------------------- */
    onCellEnter(row) {
      this.hoverRowId = row.id;
    },
    
    onCellLeave() {
      this.hoverRowId = null;
    },
    
    rowClassName({ row }) {
      const classes = [];
      
      // 添加 hover 类
      if (row.id === this.hoverRowId) {
        classes.push("row-hover");
      }
      
      // 按钮类型的菜单特殊样式
      if (row.type === "按钮") {
        classes.push("row-button");
      }
      
      return classes.join(" ");
    },

    /* -------------------------
     *  其他方法
     * ------------------------- */
    handleResize() {
      if (this.resizeTimer) clearTimeout(this.resizeTimer);
      this.resizeTimer = setTimeout(() => {
        this.updateTableHeight();
      }, 150);
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
  overflow: hidden;

  .card {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
    background: v-bind(subBackgroundColor);
    border: none;
    transition: none !important;

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

      /* 表格背景 */
      ::v-deep .el-table {
        background-color: v-bind(tableBackgroundColor);
        color: v-bind(tableTextColor);
        width: 100%;
      }

      /* 表头 */
      ::v-deep .el-table__header th {
        background-color: v-bind(tableHeaderBackgroundColor) !important;
        color: v-bind(tableHeaderTextColor) !important;
      }

      /* 行背景 */
      ::v-deep .el-table__row {
        background-color: v-bind(tableBackgroundColor) !important;
      }

      /* 单元格字体颜色 */
      ::v-deep .el-table__row td {
        color: v-bind(tableTextColor) !important;
      }

      /* -----------------------------
       * ⭐ 统一 hover 行（主表格 + 左固定列 + 右固定列）
       * ----------------------------- */
      ::v-deep .row-hover > td {
        background-color: v-bind(tableRowHoverBackgroundColor) !important;
      }

      ::v-deep .el-table__fixed .row-hover > td {
        background-color: v-bind(tableRowHoverBackgroundColor) !important;
      }

      ::v-deep .el-table__fixed-right .row-hover > td {
        background-color: v-bind(tableRowHoverBackgroundColor) !important;
      }
      
      /* -----------------------------
       * ⭐ 按钮类型菜单的特殊样式
       * ----------------------------- */
      ::v-deep .row-button > td {
        background-color: rgba(255, 152, 0, 0.05) !important;
        
        &:hover {
          background-color: rgba(255, 152, 0, 0.1) !important;
        }
      }
      
      ::v-deep .el-table__fixed .row-button > td,
      ::v-deep .el-table__fixed-right .row-button > td {
        background-color: rgba(255, 152, 0, 0.05) !important;
        
        &:hover {
          background-color: rgba(255, 152, 0, 0.1) !important;
        }
      }
      
      /* 按钮类型菜单且悬停时的样式 */
      ::v-deep .row-button.row-hover > td {
        background-color: rgba(255, 152, 0, 0.15) !important;
      }
      
      ::v-deep .el-table__fixed .row-button.row-hover > td,
      ::v-deep .el-table__fixed-right .row-button.row-hover > td {
        background-color: rgba(255, 152, 0, 0.15) !important;
      }
      
      /* 操作按钮样式调整 */
      ::v-deep .el-table__row .el-button--text {
        color: v-bind(tableTextColor);
        
        &:hover {
          opacity: 0.8;
        }
      }
      
      /* 图标颜色 */
      ::v-deep .el-table__row i[class*="el-icon"],
      ::v-deep .el-table__row i[class*="iconfont"] {
        color: v-bind(tableTextColor);
      }
    }
  }
}
</style>