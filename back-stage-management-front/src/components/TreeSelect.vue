<template>
  <div class="tree-select">
    <el-popover
      placement="bottom-start"
      width="300"
      trigger="click"
      v-model="visible"
      popper-class="tree-select-popper"
    >
      <!-- 搜索框 -->
      <el-input
        v-model="filterText"
        placeholder="搜索..."
        size="small"
        clearable
        style="margin-bottom: 8px;"
      />

      <!-- 树形结构 -->
      <el-tree
        ref="tree"
        :data="data"
        :props="defaultProps"
        node-key="id"
        :show-checkbox="multiple"
        highlight-current
        :filter-node-method="filterNode"
        @node-click="handleNodeClick"
        @check="handleCheck"
        default-expand-all
      />

      <!-- 输入框触发器 -->
      <el-input
        slot="reference"
        v-model="selectedLabels"
        :placeholder="placeholder"
        readonly
        suffix-icon="el-icon-caret-bottom"
      />
    </el-popover>
  </div>
</template>

<script>
export default {
  name: "TreeSelect",
  props: {
    value: [String, Number, Array],
    data: { type: Array, required: true },
    multiple: { type: Boolean, default: false },
    placeholder: { type: String, default: "请选择" }
  },
  data() {
    return {
      visible: false,
      filterText: "",
      selectedLabels: "",
      defaultProps: { children: "children", label: "label" }
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree?.filter(val);
    },
    value: {
      immediate: true,
      handler(val) {
        if (!val) {
          this.selectedLabels = "";
          return;
        }
        if (this.multiple && Array.isArray(val)) {
          const nodes = this.$refs.tree?.getCheckedNodes() || [];
          this.selectedLabels = this.formatGroupedLabels(nodes);
        } else {
          const node = this.findNodeById(this.data, val);
          this.selectedLabels = node ? node.label : "";
        }
      }
    },
    visible(val) {
      const popper = document.querySelector('.tree-select-popper');
      if (val) {
        // 弹窗打开，允许交互
        popper?.removeAttribute('inert');
      } else {
        // 弹窗关闭前，移除焦点
        this.$nextTick(() => {
          document.activeElement?.blur();
        });
        // 延迟设置 inert，确保动画完成后 DOM 被隐藏
        setTimeout(() => {
          popper?.setAttribute('inert', '');
        }, 300); // 与 Element UI 的 fade-in-linear 动画时长保持一致
      }
    }
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.label.includes(value);
    },
    handleNodeClick(node) {
      if (!this.multiple) {
        this.selectedLabels = node.label;
        this.$emit("input", node.id);
        this.visible = false;
      }
    },
    handleCheck() {
      if (this.multiple) {
        const nodes = this.$refs.tree.getCheckedNodes();
        this.selectedLabels = this.formatGroupedLabels(nodes);
        this.$emit("input", nodes.map(n => n.id));
      }
    },
    formatGroupedLabels(nodes) {
      const grouped = {};
      nodes.forEach(node => {
        const topParent = this.findTopParent(this.data, node.id);
        if (topParent && node.id !== topParent.id) {
          if (!grouped[topParent.label]) {
            grouped[topParent.label] = [];
          }
          grouped[topParent.label].push(node.label);
        }
      });
      return Object.keys(grouped)
        .map(parent => `${parent}: ${grouped[parent].join(", ")}`)
        .join("； ");
    },
    findTopParent(list, id, parent = null) {
      for (let item of list) {
        if (item.id === id) return parent || item;
        if (item.children) {
          const found = this.findTopParent(item.children, id, parent || item);
          if (found) return found;
        }
      }
      return null;
    },
    findNodeById(list, id) {
      for (let item of list) {
        if (item.id === id) return item;
        if (item.children) {
          const found = this.findNodeById(item.children, id);
          if (found) return found;
        }
      }
      return null;
    }
  }
};
</script>

<style scoped>
.tree-select {
  width: 300px;
}
.tree-select-popper {
  max-height: 300px;
  overflow: auto;
}
</style>
