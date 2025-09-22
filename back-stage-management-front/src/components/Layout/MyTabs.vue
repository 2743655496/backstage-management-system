<template>
  <el-row class="rowtwo">
    <!-- 左滚动按钮 -->
    <button
      v-show="canScrollLeft"
      class="btn-scroll"
      @click="scrollTags('left')"
      :disabled="scrollLeftDisabled"
    >
      <i class="el-icon-arrow-left"></i>
    </button>

    <!-- 标签容器（带滚动条） -->
    <div class="tags-container" ref="tagsContainer">
      <el-tag
        v-for="tag in TabMenu"
        :key="tag.name"
        :closable="!tag.fixed"
        :type="tag.type"
        :class="['el-tag-my', { active: isActiveTag(tag) }]"
        @click="selectTag(tag)"
        @close="handleCloseTag(tag, $event)"
      >
        <template v-if="tag.fixed">
          <i class="el-icon-lock" style="margin-right: 4px"></i>
        </template>
        {{ tag.name }}
      </el-tag>
    </div>

    <!-- 右滚动按钮 -->
    <button
      class="btn-scroll"
      @click="scrollTags('right')"
      :disabled="scrollRightDisabled"
      v-show="canScrollRight"
    >
      <i class="el-icon-arrow-right"></i>
    </button>

    <!-- 其他右侧按钮 -->
    <div class="header-right">
      <el-dropdown trigger="click">
        <button class="btn-tab">
          <i class="el-icon-arrow-down"></i>
        </button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item icon="el-icon-close">关闭</el-dropdown-item>
          <el-dropdown-item icon="el-icon-refresh-right"
            >重新加载</el-dropdown-item
          >
          <el-dropdown-item
            @click.native="toggleFixed(selectedTag)"
            :icon="selectedFixed ? 'el-icon-unlock' : 'el-icon-lock'"
          >
            {{ selectedFixed ? "取消固定" : "固定标签" }}
          </el-dropdown-item>
          <el-dropdown-item icon="iconfont icon-yuyan"
            >在新窗口打开</el-dropdown-item
          >
          <el-dropdown-item icon="iconfont icon-yuyan" divided
            >关闭左侧标签页</el-dropdown-item
          >
          <el-dropdown-item icon="iconfont icon-yuyan"
            >关闭右侧标签页</el-dropdown-item
          >
          <el-dropdown-item icon="iconfont icon-yuyan" divided
            >关闭其他标签页</el-dropdown-item
          >
          <el-dropdown-item
            icon="iconfont icon-yuyan"
            @click.native="tabOperation('clearAll')"
            >关闭全部标签页</el-dropdown-item
          >
        </el-dropdown-menu>
      </el-dropdown>
      <button class="btn-tab">
        <i class="iconfont icon-fangda"></i>
        <!-- <i class="iconfont icon-suoxiao"></i> -->
      </button>
    </div>
  </el-row>
</template>

<script>
import navigation from "@/utils/navigation";
import { mapState, mapActions } from "vuex";
export default {
  computed: {
    ...mapState("MenuStateModule", ["TabMenu"]),
    selectedFixed() {
      return this.selectedTag?.fixed || false;
    },
  },
  data() {
    return {
      scrollLeftDisabled: true,
      scrollRightDisabled: false,
      canScrollLeft: false,
      canScrollRight: false,
      selectedTag: {},
    };
  },
  methods: {
    ...mapActions("MenuStateModule", [
      "clearTabMenu",
      "toggleFixedTabMenu",
      "setCurrentMenuaddTabMenu",
    ]),
    // 滚动到标签容器末尾
    scrollToEnd() {
      this.$nextTick(() => {
        const container = this.$refs.tagsContainer;
        container.scrollLeft = container.scrollWidth;
      });
    },
    // 检查是否为激活标签
    isActiveTag(tag) {
      return this.$route.path === tag.path;
    },

    // 滚动标签容器
    scrollTags(direction) {
      const container = this.$refs.tagsContainer;
      const scrollAmount = 200; // 每次滚动距离

      if (direction === "left") {
        container.scrollLeft -= scrollAmount;
      } else {
        container.scrollLeft += scrollAmount;
      }

      // 更新按钮状态
      this.updateScrollButtons();
    },

    // 更新滚动按钮状态
    updateScrollButtons() {
      const container = this.$refs.tagsContainer;
      this.scrollLeftDisabled = container.scrollLeft <= 0;
      this.scrollRightDisabled =
        container.scrollLeft + container.clientWidth >=
        container.scrollWidth - 1;
    },

    // 选择标签
    selectTag(tag) {
      this.selectedTag = tag;
      this.setCurrentMenuaddTabMenu(tag.path);
      // 这里可以添加路由跳转逻辑
      navigation.safePush(this, tag.path);
      this.$nextTick(() => {
        this.scrollTagIntoView(tag);
      });
    },
    // 将标签滚动到可见区域
    scrollTagIntoView(tag) {
      const container = this.$refs.tagsContainer;
      const tagEl = [...container.children].find((el) =>
        el.textContent.includes(tag.name)
      );

      if (!tagEl) return;

      const containerRect = container.getBoundingClientRect();
      const tagRect = tagEl.getBoundingClientRect();

      // 判断是否需要向左滚动（标签左侧被遮挡）
      if (tagRect.left < containerRect.left) {
        container.scrollLeft -= containerRect.left - tagRect.left + 5;
      }
      // 判断是否需要向右滚动（标签右侧被遮挡）
      else if (tagRect.right > containerRect.right) {
        container.scrollLeft += tagRect.right - containerRect.right + 5;
      }
    },

    // 初始化滚动监听
    initScrollListener() {
      const container = this.$refs.tagsContainer;
      container.addEventListener("scroll", this.updateScrollButtons);
    },
    checkScrollButtons() {
      const container = this.$refs.tagsContainer;
      if (container) {
        this.canScrollRight =
          container.scrollLeft + container.clientWidth < container.scrollWidth;

        if (this.canScrollRight) {
          this.scrollToEnd();
          this.canScrollLeft = true;
        } else {
          this.canScrollLeft = false;
        }
      }
    },
    //标签页操作
    tabOperation(type) {
      if (type === "clearAll") {
        this.clearTabMenu();
      }
    },
    // 关闭标签
    handleCloseTag(tag, event) {
      event.stopPropagation(); // 阻止事件冒泡
      // // 如果是当前激活的标签，需要特殊处理
      if (this.isActiveTag(tag)) {
        // this.closeActiveTag(tag);
        console.log(123);
        // this.$store.dispatch("MenuStateModule/removeTabMenu", tag.path)
      } else {
        // this.closeInactiveTag(tag);
        console.log(456);
        // this.$store.dispatch("MenuStateModule/removeTabMenu", tag.path)
      }
    },
    //刷新初始激活
    initActive() {
      const matchedRoute = this.$route.path;
      for (let i = 0; i < this.TabMenu.length; i++) {
        const item = this.TabMenu[i];
        if (item.path === matchedRoute) {
          this.selectTag(item);
        }
      }
    },
    toggleFixed(tag) {
      this.toggleFixedTabMenu(tag.path);
    },
  },
  mounted() {
    this.checkScrollButtons();
    this.initScrollListener();
    this.updateScrollButtons();
    this.initActive();
    window.addEventListener("resize", this.checkScrollButtons);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkScrollButtons);
    const container = this.$refs.tagsContainer;
    if (container) {
      container.removeEventListener("scroll", this.updateScrollButtons);
    }
  },
  watch: {
    tags() {
      this.$nextTick(() => {
        this.checkScrollButtons();
      });
    },
    "$route.path"(newPath) {
      const matched = this.TabMenu.find((tag) => tag.path === newPath);
      if (matched) {
        this.selectedTag = matched;
      }
    },
  },
};
</script>

<style lang="less" scoped>
.rowtwo {
  border: 1px solid #ebeef5; /* 新增左侧边框 */
  display: flex;
  align-items: center;
  height: 34px;
  background: #f5f7fa;
  overflow: hidden; // 隐藏溢出的内容

  .tags-container {
    flex: 1;
    display: flex;
    overflow-x: auto;
    scroll-behavior: smooth; // 平滑滚动
    &::-webkit-scrollbar {
      display: none; // 隐藏滚动条
    }
    .el-tag-my {
      flex-shrink: 0; // 禁止标签收缩
      margin-right: 2px;
      max-width: 120px; // 限制单个标签最大宽度
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: pointer;

      &.active {
        border-color: #409eff;
        background-color: #ecf5ff;
      }
    }
  }

  .btn-scroll {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    border: none;
    background: #e4e7ed;
    border-radius: 4px;
    cursor: pointer;
    margin: 0 5px;

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  .header-right {
    flex-shrink: 0;
    margin-left: auto;
    .btn-tab {
      padding: 9px 9px;
      background-color: #fff;
      color: #333;
      border: none;
      cursor: pointer;
      font-size: 17px;
    }
    .btn-tab:hover {
      background-color: #f5f5f5;
    }
  }
}
</style>