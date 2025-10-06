<template>
  <div class="tree-select">
    <el-popover
      placement="bottom-start"
      width="300"
      trigger="click"
      v-model="visible"
      :popper-class="uniqueClass"
      :disabled="disabled"
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
        :check-strictly="checkStrictly"
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
        :disabled="disabled"
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
    checkStrictly: { type: Boolean, default: false },
    placeholder: { type: String, default: "请选择" },
    disabled: { type: Boolean, default: false }
  },
  data() {
    return {
      visible: false,
      filterText: "",
      selectedLabels: "",
      defaultProps: { 
        children: "children", 
        label: "name"
      },
      uniqueClass: `tree-select-popper-${Math.random().toString(36).substr(2, 8)}`
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree?.filter(val);
    },
    value: {
      immediate: true,
      handler(val) {
        this.updateSelectedLabels();
      }
    },
    data: {
      immediate: true,
      handler() {
        this.$nextTick(() => {
          this.updateSelectedLabels();
          this.setTreeSelection();
        });
      }
    },
    visible(val) {
      if (val) {
        this.$nextTick(() => {
          this.setTreeSelection();
        });
      }
    }
  },
  mounted() {
    this.updateSelectedLabels();
    this.setTreeSelection();
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.name.includes(value);
    },
    
    handleNodeClick(node) {
      if (!this.multiple) {
        this.selectedLabels = node.name;
        this.$emit("input", node.id);
        this.$emit("change", node.id);
        this.visible = false;
      }
    },
    
    handleCheck() {
      if (this.multiple) {
        const nodes = this.$refs.tree.getCheckedNodes();
        this.selectedLabels = nodes.map(n => n.name).join(", ");
        const checkedKeys = this.$refs.tree.getCheckedKeys();
        this.$emit("input", checkedKeys);
        this.$emit("change", checkedKeys);
      }
    },
    
    updateSelectedLabels() {
      if (!this.value) {
        this.selectedLabels = "";
        return;
      }
      
      if (this.multiple && Array.isArray(this.value)) {
        const labels = this.value.map(id => this.findNodeById(this.data, id)?.name).filter(Boolean);
        this.selectedLabels = labels.join(", ");
      } else {
        const node = this.findNodeById(this.data, this.value);
        this.selectedLabels = node ? node.name : "";
      }
    },
    
    setTreeSelection() {
      if (!this.$refs.tree) return;
      
      try {
        if (this.multiple && Array.isArray(this.value)) {
          this.$refs.tree.setCheckedKeys(this.value);
        } else if (this.value) {
          this.$refs.tree.setCurrentKey(this.value);
        } else {
          // 清除选中状态
          this.$refs.tree.setCurrentKey(null);
          if (this.multiple) {
            this.$refs.tree.setCheckedKeys([]);
          }
        }
      } catch (error) {
        console.warn("设置树选择失败:", error);
      }
    },
    
    findNodeById(list, id) {
      for (let item of list) {
        if (item.id === id) return item;
        if (item.children && item.children.length > 0) {
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
  width: 100%;
}
</style>