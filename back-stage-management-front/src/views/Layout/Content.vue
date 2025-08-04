<template>
  <div class="content">
    <div class="header">
      <i v-if="!isCollapse" class="iconfont el-icon-s-fold" @click="changeMenu" ></i>
      <i v-else class="iconfont el-icon-s-unfold" @click="changeMenu" ></i>
    </div>
    <!-- 路由出口 -->
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  props:["isCollapse"],
  methods:{
    changeMenu(){
      this.$emit('changeMenu')
    }
  }
}
</script>

<style lang="less" scoped>
.content{
  .header{
    height: 57px;
    line-height: 50px;
    display: flex;
    background-color: #1e78bf;
    align-items: center;
    .iconfont{
      font-size: 25px;
      color: white;
    }
  }
}
</style>