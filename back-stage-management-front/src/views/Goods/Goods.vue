<template>
  <div class="goods">
    <!-- 搜索区域 -->
    <div class="header">
      <el-input v-model="keyword" placeholder="请输入内容"></el-input>
      <el-button type="primary">搜索</el-button>
      <el-button type="primary">添加</el-button>
      <el-button type="primary">弹窗添加</el-button>
    </div>
    <!-- 表格 -->
    <div class="wrapper">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column prop="id" label="商品ID" width="100">
        </el-table-column>
        <el-table-column prop="title" label="商品名称" width="100" show-overflow-tooltip>
        </el-table-column>
        <el-table-column prop="price" label="商品价格" width="100">
        </el-table-column>
        <el-table-column prop="num" label="商品数量" width="100">
        </el-table-column>
        <el-table-column prop="category" label="规格类目" width="100">
        </el-table-column>
        <el-table-column prop="image" label="商品图片" show-overflow-tooltip> </el-table-column>
        <el-table-column prop="sellPoint" label="商品卖点" show-overflow-tooltip> </el-table-column>
        <el-table-column prop="descs" label="商品描述" show-overflow-tooltip> </el-table-column>
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
        <el-button @click="toggleSelection([tableData[1], tableData[2]])">全选</el-button>
        <el-button @click="toggleSelection()">取消选择</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { getGoodsList} from '@/api/index.js'
export default {
  data() {
    return {
      keyword: "",
      tableData: [
      
      ],
    };
  },
  created(){
    this.getGoodsList()
  },
  methods: {
    async getGoodsList(pageNum){
      try{
        const res = await getGoodsList({page:pageNum})
        this.tableData = res.data
      }catch (errot){

      }
    },
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    toggleSelection(rows) {

      },
    handleSelectionChange(val) {
      this.multipleSelection = val;
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