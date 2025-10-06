<template>
  <div class="role-page">
    <!-- ✅ 搜索区域 -->
    <div class="search-section" v-show="showSearchArea">
      <el-card>
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

        <div class="table-wrapper">
          <el-table
            :data="roleList"
            :height="tableHeight"
            border
            stripe
            row-key="id"
          >
            <el-table-column prop="name" label="角色名称" width="200" fixed />
            <el-table-column prop="id" label="角色ID" width="100" />
            <el-table-column
              prop="creator_name"
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
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="create_time" label="创建时间" width="180">
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

export default {
  components: {
    RoleForm,
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

      searchForm: {
        name: "",
        id: "",
        status: null,
        create_time: [],
      },
      roleList: [],
      formVisible: false,
      currentRoleId: null,
      resizeTimer: null,
      screenResizeTimer: null,
      pagination: {
        total: 0,
        pageSize: 5,
        currentPage: 1,
      },
      isSearching: false,
      cachedSearchParams: {},
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
    if (this.resizeTimer) {
      clearTimeout(this.resizeTimer);
    }
    if (this.screenResizeTimer) {
      clearTimeout(this.screenResizeTimer);
    }
  },
  methods: {
    // 新增：切换搜索区域显示/隐藏
    toggleSearchArea() {
      this.showSearchArea = !this.showSearchArea;
      this.pagination.pageSize = 10;
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

    // 检查屏幕尺寸
    checkScreenSize() {
      const width = window.innerWidth;
      this.isSmallScreen = width < 768;
      this.isMediumScreen = width >= 768 && width <= 1120;
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

    // 修改原有的 toggleSearch 方法，确保在搜索区域显示时才能操作展开/收起
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
          this.$message.error(error.response?.data?.error || "角色删除失败");
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
        }
      }
    }
  }
}
</style>