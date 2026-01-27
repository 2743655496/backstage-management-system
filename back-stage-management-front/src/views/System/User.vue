<template>
  <div class="user-page">
    <!-- 搜索区域 -->
    <div class="search-section" v-show="showSearchArea">
      <el-card class="search-card">
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
          v-permission="['menu:system:user:add_button']"
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

        <div class="table-wrapper" :style="{ height: tableHeight + 'px' }">
          <table class="user-table">
            <thead>
              <tr>
                <th class="col-avatar">头像</th>
                <th class="sticky-left col-username">用户名</th>
                <th class="col-id">用户ID</th>
                <th class="col-realname">真实姓名</th>
                <th class="col-email">邮箱</th>
                <th class="col-phone">手机号</th>
                <th class="col-department">所属部门</th>
                <th class="col-roles">角色</th>
                <th class="col-status">状态</th>
                <th class="col-last-login-time">最后登录时间</th>
                <th class="col-last-login-ip">最后登录IP</th>
                <th class="col-creator">创建人</th>
                <th class="col-create-time">创建时间</th>
                <th class="sticky-right col-actions">操作</th>
              </tr>
            </thead>

            <tbody>
              <template v-for="row in userList">
                <tr 
                  :key="row.id"
                  :class="rowStatusClass(row)"
                  @mouseenter="handleRowMouseEnter(row)"
                  @mouseleave="handleRowMouseLeave"
                >
                  <!-- 头像列 -->
                  <td class="col-avatar" align="center">
                    <div class="avatar-cell">
                      <el-avatar
                        v-if="row.avatar"
                        :size="40"
                        :src="row.avatar"
                        :alt="row.username"
                        fit="cover"
                        class="user-avatar"
                      />
                      <el-avatar
                        v-else
                        :size="40"
                        :src="defaultAvatar"
                        :alt="row.username"
                        class="user-avatar"
                      >
                        {{
                          row.username
                            ? row.username.charAt(0).toUpperCase()
                            : "U"
                        }}
                      </el-avatar>
                    </div>
                  </td>

                  <!-- 左侧固定列：用户名 -->
                  <td class="sticky-left col-username">
                    {{ row.username }}
                  </td>

                  <td class="col-id">{{ row.id }}</td>
                  <td class="col-realname">{{ row.real_name || '-' }}</td>
                  <td class="col-email">{{ row.email || '-' }}</td>
                  <td class="col-phone">{{ row.phone || '-' }}</td>
                  <td class="col-department">{{ row.department_name || '-' }}</td>
                  
                  <!-- 角色列 -->
                  <td class="col-roles">
                    <div class="roles-container">
                      <el-tag
                        v-for="role in row.roles"
                        :key="role.id"
                        :type="getRoleTagType(role.id)"
                        size="small"
                        class="role-tag"
                      >
                        {{ role.name }}
                      </el-tag>
                      <span
                        v-if="!row.roles || row.roles.length === 0"
                        class="no-roles"
                      >
                        无角色
                      </span>
                    </div>
                  </td>
                  
                  <td class="col-status" align="center">
                    <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                      {{ row.status === 1 ? "启用" : "禁用" }}
                    </el-tag>
                  </td>
                  <td class="col-last-login-time">{{ formatDateTime(row.last_login_time) }}</td>
                  <td class="col-last-login-ip">{{ row.last_login_ip || '-' }}</td>
                  <td class="col-creator">{{ row.creator_name || '-' }}</td>
                  <td class="col-create-time">{{ formatDateTime(row.create_time) }}</td>

                  <!-- 右侧固定列 -->
                  <td class="sticky-right col-actions" align="center">
                    <el-button
                    v-permission="['menu:system:user:update_button']"
                      type="text"
                      size="small"
                      style="color: #67c23a"
                      @click="editRow(row)"
                    >
                      编辑
                    </el-button>
                    <el-button
                    v-permission="['menu:system:user:delete_button']"
                      type="text"
                      size="small"
                      style="color: red"
                      @click="deleteRow(row)"
                    >
                      删除
                    </el-button>
                    <span
                      class="no-permission-tag"
                      v-permission="{
                        mode: 'not',
                        codes: [
                          'menu:system:user:delete_button',
                          'menu:system:user:update_button',
                        ],
                      }"
                      >无操作权限</span
                    >
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
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
} from "@/api/modules/System/user";
import { TimeFormatter } from "@/utils/timeFormatter";
import { mapGetters } from "vuex";

export default {
  name: "User",
  components: {
    UserForm,
    MyPagination,
  },

  computed: {
    ...mapGetters("LightModule", [
      "textColor",
      "subBackgroundColor",
      "tableBackgroundColor",
      "tableTextColor",
      "tableHeaderBackgroundColor",
      "tableHeaderTextColor",
      "tableRowHoverBackgroundColor",
      "border_color",
      "table_header_border_color",
    ]),
  },

  data() {
    return {
      tableHeight: 500,
      showSearch: true,
      isMediumScreen: false,
      isSmallScreen: false,
      showSearchArea: true,
      defaultAvatar: require("@/assets/images/horse.png"),

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
      screenResizeTimer: null,
      resizeTimer: null,
      pagination: {
        total: 0,
        pageSize: 10,
        currentPage: 1,
      },
      isSearching: false,
      cachedSearchParams: {},
      roleTagTypes: ["", "success", "info", "warning", "danger"],

      // 鼠标悬停行ID
      hoverRowId: null,
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

    if (this.screenResizeTimer) {
      clearTimeout(this.screenResizeTimer);
    }
    if (this.resizeTimer) clearTimeout(this.resizeTimer);
  },

  methods: {
    // 根据状态返回CSS类名
    rowStatusClass(row) {
      const classes = [];
      
      // 添加 hover 类
      if (row.id === this.hoverRowId) {
        classes.push('row-hover');
      }
      
      // 禁用状态的特殊样式
      if (row.status === 0) {
        classes.push('row-disabled');
      }
      
      return classes.join(' ');
    },

    // 鼠标悬停处理
    handleRowMouseEnter(row) {
      this.hoverRowId = row.id;
    },
    
    handleRowMouseLeave() {
      this.hoverRowId = null;
    },

    getRoleTagType(roleId) {
      const types = ["", "success", "info", "warning", "danger"];
      return types[roleId % types.length] || "";
    },

    toggleSearchArea() {
      this.showSearchArea = !this.showSearchArea;
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

    checkScreenSize() {
      const width = window.innerWidth;
      this.isSmallScreen = width < 768;
      this.isMediumScreen = width >= 768 && width <= 1220;
    },

    handleScreenResize() {
      if (this.screenResizeTimer) {
        clearTimeout(this.screenResizeTimer);
      }
      this.screenResizeTimer = setTimeout(() => {
        this.checkScreenSize();
        this.$nextTick(() => {
          this.updateTableHeight();
        });
      }, 150);
    },

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
        const paginationHeight = 50; // 分页器高度

        this.tableHeight =
          cardHeight - headerHeight - marginBottom - paddingFix - paginationHeight;
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

    handleSearch() {
      this.isSearching = true;
      this.pagination.currentPage = 1;
      this.cachedSearchParams = { ...this.searchForm };
      this.fetchUsers();
    },

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
  overflow: hidden;

  .search-section {
    margin-bottom: 20px;
    flex-shrink: 0;

    .search-card {
      border: none;
      transition: none !important;
      background: v-bind(subBackgroundColor);
      .form-item .label {
        flex-shrink: 0;
        font-size: 14px;
        color: v-bind(textColor);
        line-height: 32px;
        width: 80px;
        text-align: right;
        padding-right: 12px;
      }
    }

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
        color: #606266; /* 保持原样 */
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
      background: v-bind(subBackgroundColor);
      border: none;
      transition: none !important;

      .header {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
        flex-shrink: 0;
        align-items: center;
        gap: 10px;
      }

      .table-wrapper {
        flex: 1;
        min-height: 0;
        overflow: auto;
        position: relative;
        border: 1px solid v-bind(border_color);

        .user-table {
          width: 100%;
          border-collapse: collapse;
          table-layout: fixed;
          background-color: v-bind(tableBackgroundColor);
          color: v-bind(tableTextColor);
          
          // 头像单元格样式
          .avatar-cell {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60px;

            .user-avatar {
              border: 1px solid rgba(255, 255, 255, 0.1);
              background-color: rgba(255, 255, 255, 0.05);
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
              color: v-bind(tableTextColor);
              opacity: 0.6;
              font-size: 12px;
            }
          }
        }

        /* 固定表头 - 使用伪元素实现下边框 */
        thead {
          position: sticky;
          top: 0;
          z-index: 5;
        }
        
        thead::after {
          content: "";
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          height: 1px;
          background-color: v-bind(table_header_border_color);
          z-index: 7;
        }

        thead tr {
          background-color: v-bind(tableHeaderBackgroundColor);
          color: v-bind(tableHeaderTextColor);
          position: relative; /* 确保伪元素定位正确 */
        }

        th,
        td {
          padding: 8px 12px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.06);
          white-space: nowrap;
          text-overflow: ellipsis;
          overflow: hidden;
        }

        /* 行 hover */
        tbody tr:hover td {
          background-color: v-bind(tableRowHoverBackgroundColor);
        }

        /* 禁用状态的特殊样式 */
        .row-disabled td {
          background-color: rgba(245, 108, 108, 0.05) !important;
          color: #f56c6c !important;
        }

        .row-disabled:hover td {
          background-color: rgba(245, 108, 108, 0.15) !important;
        }

        /* 固定列 */
        .sticky-left {
          position: sticky;
          left: 0;
          z-index: 4;
          background-color: v-bind(tableBackgroundColor);
          box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
        }

        .sticky-right {
          position: sticky;
          right: 0;
          z-index: 4;
          background-color: v-bind(tableBackgroundColor);
          box-shadow: -2px 0 4px rgba(0, 0, 0, 0.1);
        }

        /* 禁用状态的固定列背景色 */
        .row-disabled .sticky-left,
        .row-disabled .sticky-right {
          background-color: rgba(245, 108, 108, 0.05) !important;
        }

        .row-disabled:hover .sticky-left,
        .row-disabled:hover .sticky-right {
          background-color: rgba(245, 108, 108, 0.15) !important;
        }

        /* 表头中的固定列需要有更高的 z-index */
        thead .sticky-left,
        thead .sticky-right {
          z-index: 6;
          background-color: v-bind(tableHeaderBackgroundColor);
          box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* 修复表头固定列在滚动时的样式 */
        thead .sticky-left::after,
        thead .sticky-right::after {
          content: "";
          position: absolute;
          top: 0;
          right: -4px;
          width: 4px;
          height: 100%;
          background: linear-gradient(
            90deg,
            rgba(0, 0, 0, 0.1) 0%,
            rgba(0, 0, 0, 0) 100%
          );
        }

        thead .sticky-right::after {
          right: auto;
          left: -4px;
          background: linear-gradient(
            270deg,
            rgba(0, 0, 0, 0.1) 0%,
            rgba(0, 0, 0, 0) 100%
          );
        }

        /* 列宽 */
        .col-avatar {
          width: 80px;
          min-width: 80px;
        }
        .col-username {
          width: 120px;
          min-width: 120px;
          text-align: center;
        }
        .col-id {
          width: 80px;
          min-width: 80px;
          text-align: center;
        }
        .col-realname {
          width: 100px;
          min-width: 100px;
          text-align: center;
        }
        .col-email {
          width: 180px;
          min-width: 180px;
          text-align: left;
        }
        .col-phone {
          width: 120px;
          min-width: 120px;
          text-align: left;
        }
        .col-department {
          width: 120px;
          min-width: 120px;
          text-align: center;
        }
        .col-roles {
          width: 200px;
          min-width: 200px;
          text-align: left;
        }
        .col-status {
          width: 80px;
          min-width: 80px;
        }
        .col-last-login-time {
          width: 160px;
          min-width: 160px;
          text-align: center;
        }
        .col-last-login-ip {
          width: 120px;
          min-width: 120px;
          text-align: center;
        }
        .col-creator {
          width: 100px;
          min-width: 100px;
          text-align: center;
        }
        .col-create-time {
          width: 160px;
          min-width: 160px;
          text-align: center;
        }
        .col-actions {
          width: 180px;
          min-width: 180px;
        }

        /* 修复表格滚动时的边框问题 */
        tbody tr:last-child td {
          border-bottom: none;
        }

        /* 确保固定列在滚动时不被遮挡 */
        .sticky-left,
        .sticky-right {
          position: -webkit-sticky; /* Safari 支持 */
          position: sticky;
        }

        /* Tag标签颜色适配 */
        .el-tag {
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
          &.el-tag--warning {
            background-color: rgba(230, 162, 60, 0.1);
            border-color: rgba(230, 162, 60, 0.2);
            color: #e6a23c;
          }
          &.el-tag--info {
            background-color: rgba(144, 147, 153, 0.1);
            border-color: rgba(144, 147, 153, 0.2);
            color: #909399;
          }
        }

        /* 美化滚动条 */
        &::-webkit-scrollbar {
          background: rgba(0, 0, 0, 0.05);
          width: 8px;
          height: 8px;
          &:vertical {
            border-left: 1px solid v-bind(border_color);
          }
        }
        /* 改变滚动条交叉区域背景 - 主题色 */
        &::-webkit-scrollbar-corner {
          background: rgba(0, 0, 0, 0.05);
          border-left: 1px solid v-bind(border_color);
          border-top: 1px solid v-bind(border_color);
        }

        &::-webkit-scrollbar-track {
          background: rgba(0, 0, 0, 0.05);
          border: 1px solid v-bind(border_color);
          border-right: none;
          border-bottom: none;
          border-left: none;
          margin-top: 35px;
        }

        &::-webkit-scrollbar-thumb {
          background: rgba(144, 147, 153, 0.3);
          transition: background 0.3s;

          &:hover {
            background: rgba(144, 147, 153, 0.5);
          }

          &:active {
            background: rgba(144, 147, 153, 0.7);
          }
        }
      }
    }
  }
}
</style>