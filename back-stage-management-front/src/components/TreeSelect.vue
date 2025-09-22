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
    value: [String, Number, Array], // 绑定值
    data: { type: Array, required: true }, // 树数据
    multiple: { type: Boolean, default: false }, // 是否多选
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
      this.$refs.tree.filter(val);
    },
    value: {
      immediate: true,
      handler(val) {
        if (!val) {
          this.selectedLabels = "";
          return;
        }
        if (this.multiple && Array.isArray(val)) {
          const nodes = this.$refs.tree
            ? this.$refs.tree.getCheckedNodes()
            : [];
          this.selectedLabels = this.formatGroupedLabels(nodes);
        } else {
          const node = this.findNodeById(this.data, val);
          this.selectedLabels = node ? node.label : "";
        }
      }
    }
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    handleNodeClick(node) {
      if (!this.multiple) {
        this.selectedLabels = node.label;
        this.$emit("input", node.id);
        this.visible = false; // 单选时选完收起
      }
    },
    handleCheck() {
      if (this.multiple) {
        const nodes = this.$refs.tree.getCheckedNodes();
        this.selectedLabels = this.formatGroupedLabels(nodes);
        this.$emit("input", nodes.map(n => n.id));
      }
    },
    // 格式化多选显示：按顶级父节点分组
    formatGroupedLabels(nodes) {
      const grouped = {};
      nodes.forEach(node => {
        const topParent = this.findTopParent(this.data, node.id);
        if (topParent) {
          // 跳过顶级父节点本身
          if (node.id === topParent.id) return;
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
    // 找到某个节点的顶级父节点
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