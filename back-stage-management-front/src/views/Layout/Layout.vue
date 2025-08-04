<template>
  <div class="layout">
    <!-- 左侧菜单栏 -->
    <MyMenu class="menu" :isCollapse='isCollapse'/>
    <!-- 右侧菜单栏 -->
    <Content class="content" @changeMenu='changeMenu' :isCollapse='isCollapse' :class="{isActive:isCollapse}"/>

  </div>
</template>

<script>
import Content from './Content.vue'
import MyMenu from './MyMenu.vue'
export default {
  components:{
    MyMenu,
    Content
  },
  data() {
    return {
      isCollapse: false,
    };
  },
  methods:{
    /**
     * 父组件接收事件
     */
    changeMenu(){
      this.isCollapse= !this.isCollapse
    }
  }
}
</script>

<style lang="less" scoped>
.layout{
  // display: flex;
  position: relative;
  .menu{
    position: fixed;
    // width: 200px;
    top: 0;
    bottom: 0;
    min-height: 500px;
    background-color: #4a73be;
  }
  .content{
    margin-left: 200px;
    height: 1200px;
  }
  .isActive{
    margin-left: 64px;
  }
}
</style>