<template>
  <div class="pagination">
    <el-pagination
      background
      layout="total,prev, pager, next,jumper"
      :total="total"
      :pageSize="pageSize"
      :current-page="currentPage"
      @current-change="changePageNum"
    >
    </el-pagination>
  </div>
</template>

<script>
export default {
  props: {
    total: {
      type: Number,
      default: 100,
    },
    pageSize: {
      type: Number,
      default: 1,
    },
    currentPage: {
      type: Number,
      default: 1,
    },
  },
  methods: {
    changePageNum(page) {
      this.$emit("changePageNum", page);
    },
  },
};
</script>

<style lang="less" scoped>
.pagination {
  text-align: center;
  margin: 20px;
}
</style>