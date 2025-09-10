<template>
  <div class="layout">
    <!-- 左侧菜单栏 -->
    <div class="left-side" :style="{ width: leftWidth + 'px' }">
      <MyMenu class="menu" :isCollapse='isCollapse'/>
    </div>
    <!-- 右侧菜单栏 -->
    <div class="right-side" :style="{ left: leftWidth + 'px' }">
      <Content class="content" @changeMenu='changeMenu' :isCollapse='isCollapse' :class="{isActive:isCollapse}"/>
    </div>
  </div>
</template>

<script>
import Content from './MyContent.vue'
import MyMenu from './MyMenu.vue'
import { checkAuth } from '@/utils/auth'
export default {
  components:{
    MyMenu,
    Content,
  },
  data() {
    return {
      isCollapse: false,
      leftWidth: 200, // 初始宽度200px
    };
  },
  mounted() {
    checkAuth()
  },
  methods:{
    /**
     * 父组件接收事件
     */
    changeMenu(){
      this.isCollapse= !this.isCollapse
      this.leftWidth = this.isCollapse ? 64 : 200;
    },
  }
}
</script>

<style lang="less" scoped>
.layout{
  position: relative;

  height: 100vh;
  overflow: hidden;
  background-color: #fff;
  .left-side {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    transition: width 0.4s ease;
    box-sizing: border-box;
  }
  .right-side {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    transition: left 0.4s ease;
    box-sizing: border-box;
    overflow: auto;
    border-left: 1px solid #ebeef5; /* 新增左侧边框 */
  }
}
</style>