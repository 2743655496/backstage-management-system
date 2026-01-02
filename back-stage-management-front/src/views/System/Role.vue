<template>
  <div class="role-page">
    <!-- ✅ 搜索区域 -->
    <div class="search-section" v-show="showSearchArea">
      <el-card class="search-card">
        <!-- 屏幕 > 1120px 时的布局 -->
        <div
          class="large-screen-layout"
          v-show="!isMediumScreen && !isSmallScreen"
        >
          <el-row :gutter="20">
            <el-col :span="8" class="form-item">
              <span class="label">角色名称:</span>
              <el-input
                v-model="searchForm.name"
                placeholder="请输入角色名称"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="8" class="form-item">
              <span class="label roleid">角色ID:</span>
              <el-input
                v-model="searchForm.id"
                placeholder="请输入角色ID"
                clearable
                size="small"
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
              <span class="label" v-show="showSearch"> 角色状态:</span>
              <el-select
                v-show="showSearch"
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
            <el-col :span="16" class="form-item actions-col">
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

        <!-- 768px ≤ 屏幕 ≤ 1120px 时的布局 -->
        <div
          class="medium-screen-layout"
          v-show="isMediumScreen && !isSmallScreen"
        >
          <el-row :gutter="20">
            <el-col :span="12" class="form-item">
              <span class="label">角色名称:</span>
              <el-input
                v-model="searchForm.name"
                placeholder="请输入角色名称"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
            <el-col :span="12" class="form-item" v-show="showSearch">
              <span class="label">角色ID:</span>
              <el-input
                v-model="searchForm.id"
                placeholder="请输入角色ID"
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
              <span class="label">角色状态:</span>
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
              <span class="label">角色名称:</span>
              <el-input
                v-model="searchForm.name"
                placeholder="请输入角色名称"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">角色ID:</span>
              <el-input
                v-model="searchForm.id"
                placeholder="请输入角色ID"
                clearable
                size="small"
                class="input-field"
              />
            </el-col>
          </el-row>
          <el-row :gutter="20" v-show="showSearch">
            <el-col :span="24" class="form-item">
              <span class="label">角色状态:</span>
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

    <!-- ✅ 表格展示区域 -->
    <div class="table-section">
      <el-card class="card">
        <div class="header">
          <el-button
            type="primary"
            icon="el-icon-plus"
            @click="openForm()"
            size="medium"
            >新增角色</el-button
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
          <table class="role-table">
            <thead>
              <tr>
                <th class="sticky-left col-name">角色名称</th>
                <th class="col-id">角色ID</th>
                <th class="col-creator">创建人</th>
                <th class="col-status">状态</th>
                <th class="col-description">描述</th>
                <th class="col-time">创建时间</th>
                <th class="sticky-right col-actions">操作</th>
              </tr>
            </thead>

            <tbody>
              <template v-for="row in roleList">
                <tr 
                  :key="row.id"
                  :class="rowStatusClass(row)"
                >
                  <!-- 左侧固定列：角色名称 -->
                  <td class="sticky-left col-name">
                    {{ row.name }}
                  </td>

                  <td class="col-id">{{ row.id }}</td>
                  <td class="col-creator" align="center">{{ row.creator_name || '-' }}</td>
                  <td class="col-status" align="center">
                    <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                      {{ row.status === 1 ? "启用" : "禁用" }}
                    </el-tag>
                  </td>
                  <td class="col-description">{{ row.description || '-' }}</td>
                  <td class="col-time">{{ formatDateTime(row.create_time) }}</td>

                  <!-- 右侧固定列 -->
                  <td class="sticky-right col-actions" align="center">
                    <el-button
                      type="text"
                      size="small"
                      @click="editRow(row)"
                      style="color: #67c23a"
                    >
                      编辑
                    </el-button>
                    <el-button
                      type="text"
                      size="small"
                      style="color: red"
                      @click="deleteRow(row)"
                    >
                      删除
                    </el-button>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- ✅ 分页器 -->
        <my-pagination
          :total="pagination.total"
          :pageSize="pagination.pageSize"
          :currentPage="pagination.currentPage"
          @changePageNum="handlePageChange"
        />
      </el-card>
    </div>

    <role-form
      :visible.sync="formVisible"
      :role-id="currentRoleId"
      @refresh="fetchRoles"
    />
  </div>
</template>

<script>
import RoleForm from "@/components/System/RoleForm.vue";
import MyPagination from "@/components/MyPagination.vue";
import { getRoles, toDeleteRole } from "@/api/modules/System/role";
import { TimeFormatter } from "@/utils/timeFormatter";
import { mapGetters } from "vuex";

export default {
  components: {
    RoleForm,
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

      searchForm: {
        name: "",
        id: "",
        status: null,
        create_time: [],
      },
      roleList: [],
      formVisible: false,
      currentRoleId: null,
      screenResizeTimer: null,
      pagination: {
        total: 0,
        pageSize: 10,
        currentPage: 1,
      },
      isSearching: false,
      cachedSearchParams: {},

      // 鼠标悬停行ID
      hoverRowId: null,
      resizeTimer: null,
    };
  },

  created() {
    this.fetchRoles();
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
      if (row.status === 0) {
        return 'row-disabled';
      }
      return '';
    },

    // 鼠标悬停处理
    handleRowMouseEnter(row) {
      this.hoverRowId = row.id;
    },
    
    handleRowMouseLeave() {
      this.hoverRowId = null;
    },

    toggleSearchArea() {
      this.showSearchArea = !this.showSearchArea;
      this.$nextTick(() => {
        setTimeout(() => {
          this.updateTableHeight();
        }, 50);
      });
      this.fetchRoles();
    },

    formatDateTime(time) {
      if (!time) return "";
      return TimeFormatter.formatFull(time, { useUTC: true });
    },

    checkScreenSize() {
      const width = window.innerWidth;
      this.isSmallScreen = width < 768;
      this.isMediumScreen = width >= 768 && width <= 1120;
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
      this.fetchRoles();
    },

    async fetchRoles() {
      try {
        let params = {
          page: this.pagination.currentPage,
          page_size: this.pagination.pageSize,
        };

        if (this.isSearching) {
          const searchParams = this.buildSearchParams();
          params = { ...params, ...searchParams };
        }

        const res = await getRoles(params);

        if (res.data && res.data.success) {
          this.roleList = res.data.data.results || [];
          this.pagination.total = res.data.data.count || 0;
        } else {
          throw new Error(res.data?.message || "获取数据失败");
        }
      } catch (error) {
        console.error("获取角色列表失败:", error);
      }
    },

    buildSearchParams() {
      const params = {};

      if (this.cachedSearchParams.name) {
        params.name = this.cachedSearchParams.name;
      }
      if (this.cachedSearchParams.id) {
        params.id = this.cachedSearchParams.id;
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
        name: "",
        id: "",
        status: null,
        create_time: [],
      };
      this.isSearching = false;
      this.cachedSearchParams = {};
      this.pagination.currentPage = 1;
      this.fetchRoles();
    },

    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchRoles();
    },

    openForm() {
      this.currentRoleId = null;
      this.formVisible = true;
    },

    editRow(row) {
      this.currentRoleId = row.id;
      this.formVisible = true;
    },

    async deleteRow(row) {
      try {
        await this.$confirm(`确定删除角色 ${row.name} 吗？`, "提示", {
          type: "warning",
        });

        await toDeleteRole(row.id);
        this.$message.success("角色删除成功");
        this.fetchRoles();
      } catch (error) {
        if (error !== "cancel") {
          if (!error.__handled) {
            this.$message.error(error.response?.data?.error || "角色删除失败");
          }
        }
      }
    },
  },
};
</script>

<style lang="less" scoped>
.role-page {
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
      background: v-bind(subBackgroundColor);
      border: none;
      transition: none !important;
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

    /* 搜索卡片样式 - 保持原样，不绑定主题变量 */
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

        .role-table {
          width: 100%;
          border-collapse: collapse;
          table-layout: fixed;
          background-color: v-bind(tableBackgroundColor);
          color: v-bind(tableTextColor);
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
        .col-name {
          width: 200px;
          min-width: 200px;
          text-align: center;
        }
        .col-id {
          width: 100px;
          min-width: 100px;
          text-align: center;
        }
        .col-creator {
          width: 120px;
          min-width: 120px;
        }
        .col-status {
          width: 100px;
          min-width: 100px;
        }
        .col-description {
          width: 360px;
          min-width: 360px;
          text-align: left;
        }
        .col-time {
          width: 180px;
          min-width: 180px;
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