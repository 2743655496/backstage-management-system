<template>
  <div class="menu-page">
    <el-card class="card">
      <div class="header">
        <el-button
          size="medium"
          type="primary"
          icon="el-icon-plus"
          @click="openForm()"
        >
          新增菜单
        </el-button>
      </div>

      <div class="table-wrapper" :style="{ height: tableHeight + 'px' }">
        <table class="menu-table">
          <thead>
            <tr>
              <th class="sticky-left col-title">标题</th>
              <th class="col-icon">图标</th>
              <th class="col-path">访问路径</th>
              <th class="col-component">页面组件</th>
              <th class="col-sort">排序</th>
              <th class="col-status">状态</th>
              <th class="col-visible">是否显示</th>
              <th class="sticky-right col-actions">操作</th>
            </tr>
          </thead>

          <tbody>
            <template v-for="row in flatTree">
              <tr :key="`${row.id}-${row.expanded}`">
                <!-- 左侧固定列：标题 + 缩进 + 展开按钮 -->
                <td class="sticky-left col-title">
                  <div
                    class="tree-cell"
                    :style="{ paddingLeft: row.level * 20 + 'px' }"
                  >
                    <i
                      v-if="row.hasChildren"
                      :class="
                        row.expanded
                          ? 'el-icon-arrow-down'
                          : 'el-icon-arrow-right'
                      "
                      class="toggle-btn"
                      @click="toggle(row)"
                    ></i>
                    <i
                      v-else
                      class="toggle-placeholder el-icon-arrow-right"
                      style="visibility: hidden"
                    ></i>
                    {{ row.name }}
                  </div>
                </td>

                <td class="col-icon" align="center">
                  <i :class="row.icon" />
                </td>

                <td class="col-path">{{ row.path }}</td>
                <td class="col-component">{{ row.component }}</td>

                <td class="col-sort" align="center">{{ row.sort }}</td>

                <td class="col-status" align="center">
                  <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                    {{ row.status === 1 ? "启用" : "禁用" }}
                  </el-tag>
                </td>

                <td class="col-visible" align="center">
                  <el-tag :type="row.visible === 1 ? 'success' : 'danger'">
                    {{ row.visible === 1 ? "显示" : "隐藏" }}
                  </el-tag>
                </td>

                <!-- 右侧固定列 -->
                <td class="sticky-right col-actions" align="center">
                  <el-button type="text" size="small" @click="addChild(row)">
                    新增下级
                  </el-button>
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
                    @click="deleteRow(row)"
                    style="color: red"
                  >
                    删除
                  </el-button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
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
      "border_color",
      "table_header_border_color",
    ]),

    // ⭐ 将树形结构拍平成可渲染的列表
    flatTree() {
      const result = [];

      const dfs = (nodes, level = 0, parentRef = null) => {
        nodes.forEach((node, index) => {
          // 创建节点引用，保持对原始节点的引用
          const nodeRef = {
            ...node,
            level,
            hasChildren: node.children && node.children.length > 0,
            // 关键：保持对原始节点的引用
            _originalNode: node,
          };

          result.push(nodeRef);

          // 只有当节点被展开且存在子节点时，才继续遍历子节点
          if (node.expanded && node.children && node.children.length) {
            dfs(node.children, level + 1, nodeRef);
          }
        });
      };

      dfs(this.menuTree);
      return result;
    },
  },

  data() {
    return {
      tableHeight: 500,
      formVisible: false,
      currentMenu: null,
      menuTree: [],
      resizeTimer: null,
      // 添加一个标志来触发 flatTree 重新计算
      treeVersion: 0,
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
    // 切换展开/折叠状态
    toggle(row) {
      // 直接修改原始节点的 expanded 属性
      const originalNode = row._originalNode;

      // 使用 Vue.set 确保响应式
      this.$set(originalNode, "expanded", !originalNode.expanded);

      // 增加版本号触发计算属性重新计算
      this.treeVersion++;
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

        this.tableHeight =
          cardHeight - headerHeight - marginBottom - paddingFix;
      }
    },

    fetchMenus() {
      getMenus()
        .then((res) => {
          // ⭐ 初始化 expanded 为 false（默认折叠状态）
          const initExpanded = (nodes) => {
            return nodes.map((node) => {
              // 创建新对象，确保响应式
              const newNode = {
                ...node,
                expanded: false, // 默认折叠
              };

              // 递归处理子节点
              if (newNode.children && newNode.children.length) {
                newNode.children = initExpanded(newNode.children);
              }

              return newNode;
            });
          };

          this.menuTree = initExpanded(res.data.data || []);
          // 重置版本号
          this.treeVersion = 0;
        })
        .catch((error) => {
          console.error("获取菜单数据失败:", error);
          this.$message.error("获取菜单数据失败");
        });
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
      position: relative;
      border: 1px solid v-bind(border_color);

      .menu-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        background-color: v-bind(tableBackgroundColor);
        color: v-bind(tableTextColor);
      }

      /* 固定表头 */
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
        background-color: v-bind(border_color);
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

      /* 表头单元格样式增强 */
      .table-wrapper th {
        border-bottom: 2px solid #ebeef5;
        font-weight: 600;
      }

      /* 行 hover */
      tbody tr:hover td {
        background-color: v-bind(tableRowHoverBackgroundColor);
      }

      /* 树形缩进 */
      .tree-cell {
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .toggle-btn {
        cursor: pointer;
        font-size: 12px;
        width: 12px;
        height: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: #909399;
      }

      .toggle-btn:hover {
        color: #409eff;
        transform: scale(1.1);
      }

      .toggle-placeholder {
        font-size: 12px;
        width: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
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
      .col-title {
        width: 180px;
        min-width: 180px;
        text-align: left;
      }
      .col-icon {
        width: 80px;
        min-width: 80px;
      }
      .col-path {
        width: 200px;
        min-width: 200px;
        text-align: left;
      }
      .col-component {
        width: 200px;
        min-width: 200px;
        text-align: left;
      }
      .col-sort {
        width: 80px;
        min-width: 80px;
      }
      .col-status {
        width: 100px;
        min-width: 100px;
      }
      .col-visible {
        width: 100px;
        min-width: 100px;
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

        // /* 如果需要添加边框 */
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
</style>