<template>
  <div class="department-page">
    <el-card class="card">
      <div class="header">
        <el-button
          size="medium"
          type="primary"
          icon="el-icon-plus"
          @click="openForm()"
        >
          新增部门
        </el-button>
      </div>

      <div class="table-wrapper">
        <el-table
          :data="departmentTree"
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
            label="部门名称"
            width="200"
            fixed="left"
          />

          <el-table-column prop="code" label="部门编码" />
          <el-table-column prop="description" label="描述" />
          <el-table-column
            prop="manager.real_name"
            label="负责人"
            width="120"
            align="center"
          />
          <el-table-column prop="sort" label="排序" width="80" align="center" />
          <el-table-column
            prop="creator.real_name"
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

    <department-form
      :visible.sync="formVisible"
      :department="currentDepartment"
      :departments="departmentTree"
      @refresh="fetchDepartments"
    />
  </div>
</template>

<script>
import DepartmentForm from "@/components/System/DepartmentForm.vue";
import {
  getDepartments,
  toDeleteDepartment,
} from "@/api/modules/System/department";
import { mapGetters } from "vuex";

export default {
  components: { DepartmentForm },

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
      currentDepartment: null,
      departmentTree: [],
      resizeTimer: null,

      // ⭐ 记录 hover 行
      hoverRowId: null,
    };
  },

  created() {
    this.fetchDepartments();
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
      return row.id === this.hoverRowId ? "row-hover" : "";
    },

    /* -------------------------
     *  其他逻辑保持不变
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

    fetchDepartments() {
      getDepartments()
        .then((res) => {
          this.departmentTree = res.data.data;
        })
        .catch(() => {});
    },

    openForm(row = null) {
      this.currentDepartment = row ? { ...row } : null;
      this.formVisible = true;
    },

    addChild(parentRow) {
      this.currentDepartment = {
        parent_id: parentRow.id,
        name: "",
        code: "",
        description: "",
        manager_id: null,
        sort: 0,
        status: 1,
      };
      this.formVisible = true;
    },

    editRow(row) {
      this.currentDepartment = { ...row };
      this.formVisible = true;
    },

    deleteRow(row) {
      this.$confirm(`确定删除部门 ${row.name} 吗？`, "提示", {
        type: "warning",
      })
        .then(() => {
          toDeleteDepartment(row.id)
            .then(() => {
              this.$message.success("部门删除成功");
              this.fetchDepartments();
            })
            .catch((err) => {
              if (!err.__handled) {
                this.$message.error("部门删除失败");
              }
            });
        })
        .catch(() => {});
    },
  },
};
</script>

<style lang="less" scoped>
.department-page {
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
    }
  }
}
</style>
