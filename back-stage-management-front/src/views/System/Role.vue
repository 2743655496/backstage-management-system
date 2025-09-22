<template>
  <div class="role-permission-page">
    <el-card shadow="hover">
      <div class="toolbar">
        <el-input
          v-model="search"
          placeholder="搜索角色ID或权限ID"
          clearable
          @input="fetchData"
          style="width: 300px; margin-right: 20px"
        />
        <el-button
          type="success"
          icon="el-icon-user-solid"
          @click="openRoleDialog()"
          >新增角色</el-button
        >
      </div>

      <el-table :data="tableData" stripe style="margin-top: 20px">
        <el-table-column prop="role_id" label="角色ID" sortable />
        <el-table-column prop="permission_id" label="权限ID" sortable />
        <el-table-column prop="creator_id" label="创建人ID" />
        <el-table-column prop="create_time" label="创建时间" />
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button size="mini" @click="openPermissionDialog(scope.row)"
              >编辑权限</el-button
            >
            <el-button
              size="mini"
              type="danger"
              @click="deleteItem(scope.row.id)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <pagination
        :total="total"
        :pageSize="pageSize"
        :currentPage="currentPage"
        @changePageNum="handlePageChange"
      />
    </el-card>

    <!-- 编辑权限弹窗 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="permissionDialogVisible"
      width="500px"
    >
      <el-form :model="formData" label-width="100px">
        <el-form-item label="角色ID">
          <el-input v-model="formData.role_id" />
        </el-form-item>
        <el-form-item label="权限ID">
          <el-input v-model="formData.permission_id" />
        </el-form-item>
        <el-form-item label="创建人ID">
          <el-input v-model="formData.creator_id" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitPermissionForm">保存</el-button>
      </div>
    </el-dialog>

    <!-- 新增角色弹窗 -->
    <el-dialog title="新增角色" :visible.sync="roleDialogVisible" width="400px">
      <el-form :model="roleForm" label-width="100px">
        <el-form-item label="角色名称">
          <el-input v-model="roleForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="roleForm.description" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="success" @click="submitRoleForm">创建</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import Pagination from "@/components/MyPagination.vue"; // 路径根据你的项目结构调整

export default {
  name: "RolePermission",
  components: {
    Pagination,
  },
  data() {
    return {
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      search: "",
      permissionDialogVisible: false,
      roleDialogVisible: false,
      dialogTitle: "编辑角色权限",
      formData: {
        id: null,
        role_id: "",
        permission_id: "",
        creator_id: "",
      },
      roleForm: {
        name: "",
        description: "",
      },
    };
  },
  created() {
    // this.fetchData()
  },
  methods: {
    async fetchData() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize,
        search: this.search,
      };
      const res = await axios.get("/api/role-permissions/", { params });
      this.tableData = res.data.results;
      this.total = res.data.count;
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchData();
    },
    openPermissionDialog(row) {
      this.dialogTitle = "编辑角色权限";
      this.formData = { ...row };
      this.permissionDialogVisible = true;
    },
    async submitPermissionForm() {
      if (this.formData.id) {
        await axios.put(
          `/api/role-permissions/${this.formData.id}/`,
          this.formData
        );
      }
      this.permissionDialogVisible = false;
      this.fetchData();
    },
    async deleteItem(id) {
      await this.$confirm("确认删除该记录？", "提示", { type: "warning" });
      await axios.delete(`/api/role-permissions/${id}/`);
      this.fetchData();
    },
    openRoleDialog() {
      this.roleForm = { name: "", description: "" };
      this.roleDialogVisible = true;
    },
    async submitRoleForm() {
      await axios.post("/api/roles/", this.roleForm);
      this.roleDialogVisible = false;
      this.$message.success("角色创建成功");
    },
  },
};
</script>

<style scoped>
.role-permission-page {
  padding: 20px;
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
