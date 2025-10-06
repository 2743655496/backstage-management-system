<template>
  <div class="user-page">
    <!-- 搜索区域 -->
    <div class="search-section" v-show="showSearchArea">
      <el-card>
        <!-- 屏幕 > 1220px 时的布局 -->
        <div
          class="large-screen-layout"
          v-show="!isMediumScreen && !isSmallScreen"
        >
          <el-row :gutter="20">
            <el-col :span="8" class="form-item">
              <span class="label">用户名称:</span>
              <el-input
                v-model="searchForm.username"
                placeholder="请输入用户名"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="8" class="form-item">
              <span class="label">用户ID:</span>
              <el-input
                v-model="searchForm.id"
                placeholder="请输入用户ID"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="8" class="form-item actions-col">
              <div class="search-actions-wrapper" v-show="!showSearch">
                <el-button
                  type="primary"
                  icon="el-icon-search"
                  size="small"
                  @click="handleSearch"
                  >搜索</el-button
                >
                <el-button
                  icon="el-icon-refresh"
                  size="small"
                  @click="resetSearch"
                  >重置</el-button
                >
                <el-button type="text" size="small" @click="toggleSearch">
                  {{ showSearch ? "收起搜索" : "展开搜索" }}
                  <i
                    :class="
                      showSearch ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
                    "
                  ></i>
                </el-button>
              </div>
              <span class="label" v-show="showSearch">手机号:</span>
              <el-input
                v-show="showSearch"
                v-model="searchForm.phone"
                placeholder="请输入手机号"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="8" class="form-item">
              <span class="label" v-show="showSearch"> 真实姓名:</span>
              <el-input
                v-show="showSearch"
                v-model="searchForm.real_name"
                placeholder="请输入真实姓名"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="8" class="form-item">
              <span class="label">状态:</span>
              <el-select
                v-model="searchForm.status"
                placeholder="请选择状态"
                clearable
                size="small"
                class="input-field"
              >
                <el-option label="启用" :value="1" />
                <el-option label="禁用" :value="0" />
              </el-select>
            </el-col>
            <el-col :span="8" class="form-item">
              <span class="label">创建时间:</span>
              <el-date-picker
                v-model="searchForm.create_time"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item actions-col">
              <div class="search-actions-wrapper">
                <el-button
                  type="primary"
                  icon="el-icon-search"
                  size="small"
                  @click="handleSearch"
                  >搜索</el-button
                >
                <el-button
                  icon="el-icon-refresh"
                  size="small"
                  @click="resetSearch"
                  >重置</el-button
                >
                <el-button type="text" size="small" @click="toggleSearch">
                  {{ showSearch ? "收起搜索" : "展开搜索" }}
                  <i
                    :class="
                      showSearch ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
                    "
                  ></i>
                </el-button>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 768px ≤ 屏幕 ≤ 1220px 时的布局 -->
        <div
          class="medium-screen-layout"
          v-show="isMediumScreen && !isSmallScreen"
        >
          <el-row :gutter="20">
            <el-col :span="12" class="form-item">
              <span class="label">用户名称:</span>
              <el-input
                v-model="searchForm.username"
                placeholder="请输入用户名"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="12" class="form-item" v-show="showSearch">
              <span class="label">用户ID:</span>
              <el-input
                v-model="searchForm.id"
                placeholder="请输入用户ID"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col
              :span="12"
              class="form-item actions-col"
              v-show="!showSearch"
            >
              <div class="search-actions-wrapper">
                <el-button
                  type="primary"
                  icon="el-icon-search"
                  size="small"
                  @click="handleSearch"
                  >搜索</el-button
                >
                <el-button
                  icon="el-icon-refresh"
                  size="small"
                  @click="resetSearch"
                  >重置</el-button
                >
                <el-button type="text" size="small" @click="toggleSearch">
                  {{ showSearch ? "收起搜索" : "展开搜索" }}
                  <i
                    :class="
                      showSearch ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
                    "
                  ></i>
                </el-button>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="12" class="form-item">
              <span class="label">手机号:</span>
              <el-input
                v-model="searchForm.phone"
                placeholder="请输入手机号"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="12" class="form-item">
              <span class="label">真实姓名:</span>
              <el-input
                v-model="searchForm.real_name"
                placeholder="请输入真实姓名"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="12" class="form-item">
              <span class="label">状态:</span>
              <el-select
                v-model="searchForm.status"
                placeholder="请选择状态"
                clearable
                size="small"
                class="input-field"
              >
                <el-option label="启用" :value="1" />
                <el-option label="禁用" :value="0" />
              </el-select>
            </el-col>
            <el-col :span="12" class="form-item">
              <span class="label">创建时间:</span>
              <el-date-picker
                v-model="searchForm.create_time"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item actions-col">
              <div class="search-actions-wrapper">
                <el-button
                  type="primary"
                  icon="el-icon-search"
                  size="small"
                  @click="handleSearch"
                  >搜索</el-button
                >
                <el-button
                  icon="el-icon-refresh"
                  size="small"
                  @click="resetSearch"
                  >重置</el-button
                >
                <el-button type="text" size="small" @click="toggleSearch">
                  {{ showSearch ? "收起搜索" : "展开搜索" }}
                  <i
                    :class="
                      showSearch ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
                    "
                  ></i>
                </el-button>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 屏幕 < 768px 时的布局 -->
        <div class="small-screen-layout" v-show="isSmallScreen">
          <el-row :gutter="20">
            <el-col :span="24" class="form-item">
              <span class="label">用户名称:</span>
              <el-input
                v-model="searchForm.username"
                placeholder="请输入用户名"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">用户ID:</span>
              <el-input
                v-model="searchForm.id"
                placeholder="请输入用户ID"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">手机号:</span>
              <el-input
                v-model="searchForm.phone"
                placeholder="请输入手机号"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">真实姓名:</span>
              <el-input
                v-model="searchForm.real_name"
                placeholder="请输入真实姓名"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">状态:</span>
              <el-select
                v-model="searchForm.status"
                placeholder="请选择状态"
                clearable
                size="small"
                class="input-field"
              >
                <el-option label="启用" :value="1" />
                <el-option label="禁用" :value="0" />
              </el-select>
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">创建时间:</span>
              <el-date-picker
                v-model="searchForm.create_time"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24" class="form-item actions-col">
              <div class="search-actions-wrapper">
                <el-button
                  type="primary"
                  icon="el-icon-search"
                  size="small"
                  @click="handleSearch"
                  >搜索</el-button
                >
                <el-button
                  icon="el-icon-refresh"
                  size="small"
                  @click="resetSearch"
                  >重置</el-button
                >
                <el-button type="text" size="small" @click="toggleSearch">
                  {{ showSearch ? "收起搜索" : "展开搜索" }}
                  <i
                    :class="
                      showSearch ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
                    "
                  ></i>
                </el-button>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- 表格展示区域 -->
    <div class="table-section">
      <el-card class="card">
        <div class="header">
          <el-button
            type="primary"
            icon="el-icon-plus"
            @click="openForm()"
            size="medium"
            >新增用户</el-button
          >
          <!-- 新增的搜索切换按钮 -->
          <el-button
            circle
            :type="showSearchArea ? 'primary' : ''"
            icon="el-icon-search"
            @click="toggleSearchArea"
            size="medium"
            class="search-toggle-btn"
          />
        </div>

        <div class="table-wrapper">
          <el-table
            :data="userList"
            :height="tableHeight"
            border
            stripe
            row-key="id"
          >
            <!-- 新增头像列 -->
            <el-table-column label="头像" width="80" align="center">
              <template slot-scope="scope">
                <div class="avatar-cell">
                  <el-avatar
                    v-if="scope.row.avatar"
                    :size="40"
                    :src="scope.row.avatar"
                    :alt="scope.row.username"
                    fit="cover"
                    class="user-avatar"
                  />
                  <el-avatar
                    v-else
                    :size="40"
                    :src="defaultAvatar"
                    :alt="scope.row.username"
                    class="user-avatar"
                  >
                    {{
                      scope.row.username
                        ? scope.row.username.charAt(0).toUpperCase()
                        : "U"
                    }}
                  </el-avatar>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="username" label="用户名" width="120" fixed />
            <el-table-column prop="id" label="用户ID" width="80" />
            <el-table-column prop="real_name" label="真实姓名" width="100" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column prop="phone" label="手机号" width="120" />
            <el-table-column
              prop="department_name"
              label="所属部门"
              width="120"
            />
            
            <!-- 新增角色列 -->
            <el-table-column label="角色" width="200">
              <template slot-scope="scope">
                <div class="roles-container">
                  <el-tag
                    v-for="role in scope.row.roles"
                    :key="role.id"
                    :type="getRoleTagType(role.id)"
                    size="small"
                    class="role-tag"
                  >
                    {{ role.name }}
                  </el-tag>
                  <span v-if="!scope.row.roles || scope.row.roles.length === 0" class="no-roles">
                    无角色
                  </span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column
              prop="status"
              label="状态"
              width="80"
              align="center"
            >
              <template slot-scope="scope">
                <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
                  {{ scope.row.status === 1 ? "启用" : "禁用" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              prop="last_login_time"
              label="最后登录时间"
              width="160"
            >
              <template slot-scope="scope">
                {{ formatDateTime(scope.row.last_login_time) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="last_login_ip"
              label="最后登录IP"
              width="120"
            />
            <el-table-column prop="creator_name" label="创建人" width="100" />
            <el-table-column prop="create_time" label="创建时间" width="160">
              <template slot-scope="scope">
                {{ formatDateTime(scope.row.create_time) }}
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              width="180"
              align="center"
              fixed="right"
            >
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="editRow(scope.row)"
                  >编辑</el-button
                >
                <el-button
                  v-if="scope.row.status === 0"
                  type="text"
                  size="small"
                  style="color: #67c23a"
                  @click="enableUser(scope.row)"
                  >启用</el-button
                >
                <el-button
                  type="text"
                  size="small"
                  style="color: red"
                  @click="deleteRow(scope.row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 分页器 -->
        <my-pagination
          :total="pagination.total"
          :pageSize="pagination.pageSize"
          :currentPage="pagination.currentPage"
          @changePageNum="handlePageChange"
        />
      </el-card>
    </div>

    <user-form
      :visible.sync="formVisible"
      :user-id="currentUserId"
      @refresh="fetchUsers"
    />
  </div>
</template>

<script>
import UserForm from "@/components/System/UserForm.vue";
import MyPagination from "@/components/MyPagination.vue";
import {
  getUsers,
  toDeleteUser,
  toEnableUser,
  toDisableUser,
} from "@/api/modules/System/user";
import { TimeFormatter } from "@/utils/timeFormatter";

export default {
  name: "User",
  components: {
    UserForm,
    MyPagination,
  },
  data() {
    return {
      tableHeight: 500,
      showSearch: true,
      isMediumScreen: false,
      isSmallScreen: false,
      // 新增：控制搜索区域显示/隐藏
      showSearchArea: true,
      // 默认头像
      defaultAvatar: require("@/assets/images/horse.png"), // 需要准备一个默认头像图片

      searchForm: {
        username: "",
        id: "",
        real_name: "",
        phone: "",
        status: null,
        create_time: [],
      },
      userList: [],
      formVisible: false,
      currentUserId: null,
      resizeTimer: null,
      screenResizeTimer: null,
      // 分页数据
      pagination: {
        total: 0,
        pageSize: 10,
        currentPage: 1,
      },
      // 搜索状态标识
      isSearching: false,
      // 缓存搜索条件
      cachedSearchParams: {},
      // 角色标签类型映射
      roleTagTypes: ['', 'success', 'info', 'warning', 'danger']
    };
  },
  created() {
    this.fetchUsers();
    this.checkScreenSize();
  },
  mounted() {
    this.$nextTick(() => {
      this.updateTableHeight();
      window.addEventListener("resize", this.handleResize);
      window.addEventListener("resize", this.handleScreenResize);
    });
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
    window.removeEventListener("resize", this.handleScreenResize);
    if (this.resizeTimer) {
      clearTimeout(this.resizeTimer);
    }
    if (this.screenResizeTimer) {
      clearTimeout(this.screenResizeTimer);
    }
  },
  methods: {
    // 获取角色标签类型
    getRoleTagType(roleId) {
      const types = ['', 'success', 'info', 'warning', 'danger'];
      return types[roleId % types.length] || '';
    },

    // 新增：切换搜索区域显示/隐藏
    toggleSearchArea() {
      this.showSearchArea = !this.showSearchArea;
      this.pagination.pageSize = 10;
      this.$nextTick(() => {
        setTimeout(() => {
          this.updateTableHeight();
        }, 50);
      });
      this.fetchUsers();
    },
    formatDateTime(time) {
      if (!time) return "";
      return TimeFormatter.formatFull(time, { useUTC: true });
    },

    // 检查屏幕尺寸
    checkScreenSize() {
      const width = window.innerWidth;
      this.isSmallScreen = width < 768;
      this.isMediumScreen = width >= 768 && width <= 1220;
    },

    // 屏幕尺寸变化处理
    handleScreenResize() {
      if (this.screenResizeTimer) {
        clearTimeout(this.screenResizeTimer);
      }
      this.screenResizeTimer = setTimeout(() => {
        this.checkScreenSize();
        this.updateTableHeight();
      }, 150);
    },

    handleResize() {
      if (this.resizeTimer) {
        clearTimeout(this.resizeTimer);
      }
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
          cardHeight - headerHeight - marginBottom - paddingFix - 50;
      }
    },

    toggleSearch() {
      if (!this.showSearchArea) return;
      this.showSearch = !this.showSearch;
      this.$nextTick(() => {
        setTimeout(() => {
          this.updateTableHeight();
        }, 50);
      });
    },

    // 搜索处理
    handleSearch() {
      this.isSearching = true;
      this.pagination.currentPage = 1;
      this.cachedSearchParams = { ...this.searchForm };
      this.fetchUsers();
    },

    // 获取用户列表
    async fetchUsers() {
      try {
        let params = {
          page: this.pagination.currentPage,
          page_size: this.pagination.pageSize,
        };

        if (this.isSearching) {
          const searchParams = this.buildSearchParams();
          params = { ...params, ...searchParams };
        }

        const res = await getUsers(params);

        if (res.data && res.data.success) {
          this.userList = res.data.data.results || [];
          this.pagination.total = res.data.data.count || 0;
        } else {
          throw new Error(res.data?.message || "获取数据失败");
        }
      } catch (error) {
        console.error("获取用户列表失败:", error);
        this.$message.error("获取用户列表失败");
      }
    },

    // 构建搜索参数
    buildSearchParams() {
      const params = {};

      if (this.cachedSearchParams.username) {
        params.username = this.cachedSearchParams.username;
      }
      if (this.cachedSearchParams.id) {
        params.id = this.cachedSearchParams.id;
      }
      if (this.cachedSearchParams.real_name) {
        params.real_name = this.cachedSearchParams.real_name;
      }
      if (this.cachedSearchParams.phone) {
        params.phone = this.cachedSearchParams.phone;
      }
      if (
        this.cachedSearchParams.status !== null &&
        this.cachedSearchParams.status !== ""
      ) {
        params.status = this.cachedSearchParams.status;
      }

      if (
        this.cachedSearchParams.create_time &&
        this.cachedSearchParams.create_time.length === 2
      ) {
        params.create_time_start = this.cachedSearchParams.create_time[0];
        params.create_time_end = this.cachedSearchParams.create_time[1];
      }

      return params;
    },

    // 重置搜索
    resetSearch() {
      this.searchForm = {
        username: "",
        id: "",
        real_name: "",
        phone: "",
        status: null,
        create_time: [],
      };
      this.isSearching = false;
      this.cachedSearchParams = {};
      this.pagination.currentPage = 1;
      this.fetchUsers();
    },

    // 分页变化处理
    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchUsers();
    },

    openForm() {
      this.currentUserId = null;
      this.formVisible = true;
    },

    editRow(row) {
      this.currentUserId = row.id;
      this.formVisible = true;
    },

    async deleteRow(row) {
      try {
        await this.$confirm(`确定删除用户 "${row.username}" 吗？`, "提示", {
          type: "warning",
        });

        await toDeleteUser(row.id);
        this.$message.success("用户删除成功");
        this.fetchUsers();
      } catch (error) {
        if (error !== "cancel") {
          this.$message.error(error.response?.data?.error || "用户删除失败");
        }
      }
    },

    async enableUser(row) {
      try {
        await toEnableUser(row.id);
        this.$message.success("用户启用成功");
        this.fetchUsers();
      } catch (error) {
        this.$message.error(error.response?.data?.error || "启用失败");
      }
    },
  },
};
</script>

<style lang="less" scoped>
.user-page {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  height: 100%;
  background-color: #f9f9f9;
  overflow: hidden;

  .search-section {
    margin-bottom: 20px;
    flex-shrink: 0;

    ::v-deep .el-card .el-card__body {
      padding: 20px;
      margin-bottom: -20px;
      padding-left: -0px;
    }

    .form-item {
      display: flex;
      align-items: center;
      margin-bottom: 16px;

      .label {
        flex-shrink: 0;
        font-size: 14px;
        color: #606266;
        line-height: 32px;
        width: 80px;
        text-align: right;
        padding-right: 12px;
      }

      .input-field {
        flex: 1;
        min-width: 0;
      }
    }

    .actions-col {
      display: flex;
      justify-content: flex-end;
      align-items: center;

      .search-actions-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;
      }
    }

    /* 中等屏幕样式 */
    .medium-screen-layout {
      .form-item {
        .label {
          width: 70px;
        }
      }
    }
  }

  .table-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;

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

          // 头像单元格样式
          .avatar-cell {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60px;

            .user-avatar {
              border: 1px solid #ebeef5;
              background-color: white;
            }
          }

          // 角色标签样式
          .roles-container {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            align-items: center;
            
            .role-tag {
              margin: 1px;
            }
            
            .no-roles {
              color: #909399;
              font-size: 12px;
            }
          }
        }
      }
    }
  }
}
</style>