<template>
  <div class="permission-page">
    <el-card class="card">
      <div class="header">
        <el-button
          size="medium"
          type="primary"
          icon="el-icon-plus"
          @click="openForm()"
        >
          新增权限
        </el-button>
      </div>

      <div class="table-wrapper">
        <el-table
          :data="permissionTree"
          :height="tableHeight"
          row-key="id"
          border
          :tree-props="{ children: 'children' }"
          @cell-mouse-enter="onCellEnter"
          @cell-mouse-leave="onCellLeave"
          :row-class-name="rowClassName"
        >
          <!-- ✅ 左侧固定列 -->
          <el-table-column 
            prop="name" 
            label="权限名称" 
            width="200" 
            fixed="left" 
          />

          <!-- 中间普通列 -->
          <el-table-column prop="code" label="权限标识" width="200" />
          <el-table-column prop="type" label="类型" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="typeTag(scope.row.type)">
                {{ typeLabel(scope.row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="api_method"
            label="接口方法"
            width="100"
            align="center"
          />
          <el-table-column prop="api_path" label="接口路径" width="250" />
          <el-table-column prop="description" label="描述" width="200" />
          <el-table-column
            prop="creator.username"
            label="创建人"
            width="120"
            align="center"
          />
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

          <!-- ✅ 右侧固定列 -->
          <el-table-column
            label="操作"
            width="180"
            align="center"
            fixed="right"
          >
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="addChild(scope.row)">
                新增下级
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="editRow(scope.row)"
                style="color: #67c23a"
              >
                编辑
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="deleteRow(scope.row)"
                style="color: red"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <permission-form
      :visible.sync="formVisible"
      :permission="currentPermission"
      :permissions="permissionTree"
      @refresh="fetchPermissions"
    />
  </div>
</template>

<script>
import PermissionForm from "@/components/System/PermissionForm.vue";
import {
  getPermissions,
  toDeletePermission,
} from "@/api/modules/System/permission";
import { mapGetters } from "vuex";

export default {
  components: { PermissionForm },
  
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
      currentPermission: null,
      permissionTree: [],
      resizeTimer: null,
      
      // ⭐ 记录 hover 行
      hoverRowId: null,
    };
  },
  
  created() {
    this.fetchPermissions();
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
      
      // 按钮类型权限特殊样式
      if (row.type === 3) {
        classes.push("row-button");
      }
      
      // 接口类型权限特殊样式
      if (row.type === 2) {
        classes.push("row-api");
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
    
    fetchPermissions() {
      getPermissions()
        .then((res) => {
          this.permissionTree = res.data.data;
        })
        .catch(() => {});
    },
    
    openForm(row = null) {
      this.currentPermission = row ? { ...row } : null;
      this.formVisible = true;
    },
    
    addChild(parentRow) {
      this.currentPermission = {
        parent_id: parentRow.id,
        name: "",
        code: "",
        type: 3,
        api_method: "",
        api_path: "",
        description: "",
        status: 1,
      };
      this.formVisible = true;
    },
    
    editRow(row) {
      this.currentPermission = { ...row };
      this.formVisible = true;
    },
    
    deleteRow(row) {
      this.$confirm(`确定删除权限 ${row.name} 吗？`, "提示", {
        type: "warning",
      })
        .then(() => {
          toDeletePermission(row.id)
            .then(() => {
              this.$message.success("权限删除成功");
              this.fetchPermissions();
            })
            .catch((err) => {
              this.$message.error(err.response?.data?.error || "权限删除失败");
            });
        })
        .catch(() => {});
    },
    
    typeLabel(type) {
      return (
        {
          1: "菜单权限",
          2: "接口权限",
          3: "按钮权限",
        }[type] || "未知"
      );
    },
    
    typeTag(type) {
      return (
        {
          1: "primary",
          2: "warning",
          3: "success",
        }[type] || "default"
      );
    },
  },
};
</script>

<style lang="less" scoped>
.permission-page {
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
       * ⭐ 按钮类型权限的特殊样式（type=3）
       * ----------------------------- */
      ::v-deep .row-button > td {
        background-color: rgba(103, 194, 58, 0.05) !important;
        
        &:hover {
          background-color: rgba(103, 194, 58, 0.1) !important;
        }
      }
      
      ::v-deep .el-table__fixed .row-button > td,
      ::v-deep .el-table__fixed-right .row-button > td {
        background-color: rgba(103, 194, 58, 0.05) !important;
        
        &:hover {
          background-color: rgba(103, 194, 58, 0.1) !important;
        }
      }
      
      /* 按钮类型权限且悬停时的样式 */
      ::v-deep .row-button.row-hover > td {
        background-color: rgba(103, 194, 58, 0.15) !important;
      }
      
      ::v-deep .el-table__fixed .row-button.row-hover > td,
      ::v-deep .el-table__fixed-right .row-button.row-hover > td {
        background-color: rgba(103, 194, 58, 0.15) !important;
      }
      
      /* -----------------------------
       * ⭐ 接口类型权限的特殊样式（type=2）
       * ----------------------------- */
      ::v-deep .row-api > td {
        background-color: rgba(230, 162, 60, 0.05) !important;
        
        &:hover {
          background-color: rgba(230, 162, 60, 0.1) !important;
        }
      }
      
      ::v-deep .el-table__fixed .row-api > td,
      ::v-deep .el-table__fixed-right .row-api > td {
        background-color: rgba(230, 162, 60, 0.05) !important;
        
        &:hover {
          background-color: rgba(230, 162, 60, 0.1) !important;
        }
      }
      
      /* 接口类型权限且悬停时的样式 */
      ::v-deep .row-api.row-hover > td {
        background-color: rgba(230, 162, 60, 0.15) !important;
      }
      
      ::v-deep .el-table__fixed .row-api.row-hover > td,
      ::v-deep .el-table__fixed-right .row-api.row-hover > td {
        background-color: rgba(230, 162, 60, 0.15) !important;
      }
      
      /* 操作按钮样式调整 */
      ::v-deep .el-table__row .el-button--text {
        color: v-bind(tableTextColor);
        
        &:hover {
          opacity: 0.8;
        }
      }
      
      /* Tag标签颜色适配 */
      ::v-deep .el-tag {
        &.el-tag--primary {
          background-color: rgba(64, 158, 255, 0.1);
          border-color: rgba(64, 158, 255, 0.2);
          color: #409eff;
        }
        &.el-tag--warning {
          background-color: rgba(230, 162, 60, 0.1);
          border-color: rgba(230, 162, 60, 0.2);
          color: #e6a23c;
        }
        &.el-tag--success {
          background-color: rgba(103, 194, 58, 0.1);
          border-color: rgba(103, 194, 58, 0.2);
          color: #67c23a;
        }
        &.el-tag--danger {
          background-color: rgba(245, 108, 108, 0.1);
          border-color: rgba(245, 108, 108, 0.2);
          color: #f56c6c;
        }
      }
    }
  }
}
</style>