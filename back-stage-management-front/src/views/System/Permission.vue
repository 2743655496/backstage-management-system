<template>
  <div class="permission-page">
    <el-card class="card">
      <div class="header">
        <el-button type="primary" icon="el-icon-plus" @click="openForm()">
          新增权限
        </el-button>
      </div>

      <el-table
        :data="permissionTree"
        row-key="id"
        height="500"
        border
        stripe
        :tree-props="{ children: 'children' }"
        :row-class-name="rowClassName"
      >
        <!-- ✅ 固定第一列 -->
        <el-table-column
          prop="name"
          label="权限名称"
          width="200"
          fixed="left"
        />

        <el-table-column prop="code" label="权限标识" />
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
          width="80"
          align="center"
        />
        <el-table-column prop="api_path" label="接口路径" />
        <el-table-column prop="description" label="描述" />
        <el-table-column
          prop="creator.username"
          label="创建人"
          width="120"
          align="center"
        />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
              {{ scope.row.status === 1 ? "启用" : "禁用" }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- ✅ 固定最后一列 -->
        <el-table-column label="操作" width="180" align="center" fixed="right">
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
import { getPermissions, toDeletePermission } from "@/api/modules/permission";

export default {
  components: { PermissionForm },
  data() {
    return {
      formVisible: false,
      currentPermission: null,
      permissionTree: [],
    };
  },
  created() {
    this.fetchPermissions();
  },
  methods: {
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
      }).then(() => {
        toDeletePermission(row.id)
          .then(() => {
            this.$message.success("权限删除成功");
            this.fetchPermissions();
          })
          .catch((err) => {
            this.$message.error(err.response?.data?.error || "权限删除失败");
          });
      }).catch(() => {
          // 用户取消删除
        });
    },
    rowClassName({ row }) {
      return row.type === 3 ? "row-button" : "";
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
          3: "info",
        }[type] || "default"
      );
    },
  },
};
</script>

<style lang="less" scoped>
.permission-page {
  height: 93.7380104%;
  margin: 20px;
  background-color: #f9f9f9;
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
