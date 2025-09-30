<template>
  <div class="goods">
    <!-- 搜索区域 -->
    <div class="header">
      <el-input
        v-model="keyword"
        placeholder="请输入内容"
        @change="toSearch"
      ></el-input>
      <el-button type="primary">搜索</el-button>
      <el-button type="primary" @click='toAdd'>添加</el-button>
      <el-button type="primary" @click="addDialog">弹窗添加</el-button>
    </div>
    <!-- 表格 -->
    <div class="wrapper">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column type="selection" width="55"> </el-table-column>
        <el-table-column prop="id" label="商品ID" width="100">
        </el-table-column>
        <el-table-column
          prop="title"
          label="商品名称"
          width="100"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column prop="price" label="商品价格" width="100">
        </el-table-column>
        <el-table-column prop="num" label="商品数量" width="100">
        </el-table-column>
        <el-table-column prop="category" label="规格类目" width="100">
        </el-table-column>
        <el-table-column prop="image" label="商品图片" show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="sellPoint"
          label="商品卖点"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column prop="descs" label="商品描述" show-overflow-tooltip>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
              >编辑</el-button
            >
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 20px">
        <el-button @click="toggleSelection([tableData[1], tableData[2]])"
          >全选</el-button
        >
        <el-button @click="toggleSelection()">取消选择</el-button>
      </div>
    </div>
    <!-- 按钮区域 -->

    <!-- 分页 -->
    <MyPagination
      :total="total"
      :pageSize="pageSize"
      :currentPage="currentPage"
      @changePageNum="getPageNum"
    />
    <!-- 显示弹框 -->
    <GoodsDialog ref="dialog" title='商品添加'/>
  </div>
</template>

<script>
import MyPagination from "@/components/MyPagination.vue";
import { getGoodsList, getSearchList } from "@/api/modules/login.js";
import GoodsDialog from './GoodsDialog.vue';
export default {
  components: {
    MyPagination,
    GoodsDialog
  },
  data() {
    return {
      keyword: "",
      tableData: [],
      total: 10,
      pageSize: 1,
      currentPage: 1, //当前页
      searchList: [], //搜索列表
      type: 1, //1:查询所有商品分页 2:查询搜索列表的分页
    };
  },
  created() {
    // this.getGoodsList()
  },
  methods: {
    /**
     * 根据页码查询商品列表
     */
    async getGoodsList(pageNum) {
      try {
        const res = await getGoodsList({ page: pageNum });
        this.tableData = res.data;
        this.total = res.total;
        this.pageSize = res.pageSize;
      } catch (errot) {}
    },
    /**
     * 去搜索
     */

    async toSearch(val) {
      if (!val) {
        this.getGoodsList(i);
        this.type = 1;
        this.currentPage = 1;
        return;
      }

      try {
        const res = await getSearchList({ search: val });
        console.log(res);
        // 可能上千条，一次性请求增加服务器压力和前端渲染效率
        if (res.status == 200 && res.result.length != 0) {
          this.searchList = res.result;
          this.tableData = this.searchList.slice(0, 3);
          // this.tableData = res.result;

          this.total = res.result.length; //总条数
          this.pageSize = 3; //一页显示3条
          this.currentPage = 1;
          this.type = 2; //按搜索分页
        } else {
          //无数据处理
          this.tableData = [];
          this.total = 1;
          this.pageSize = 1;
          this.type = 1;
        }
      } catch (error) {
        //无数据处理
        this.tableData = [];
        this.total = 1;
        this.pageSize = 1;
        console.log(error);
        this.type = 1;
      }
    },
    /**
     * 父组件接收 分页子组件传递过来的页码
     */
    getPageNum(page) {
      this.currentPage = page;
      if (this.type == 1) {
        this.getGoodsList(page);
      } else {
        //搜索分页，切割数据
        this.tableData = this.searchList.slice((page - 1) * 3, page * 3);
      }
    },
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    toggleSelection(rows) {},
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    /**
     * 调整到新页面去添加
     */
    toAdd(){
      this.$router.push("/add-goods")
    },
    /**
     * 弹框添加
     */
    addDialog(){
      this.$refs.dialog.dialogVisible=true
    }
  },
};
</script>

<style lang="less" scoped>
.goods {
  padding: 20px;
  .header {
    padding: 20px;
    display: flex;
    button {
      margin-left: 20px;
    }
  }
  .wrapper {
    padding: 20px;
  }
}
</style>