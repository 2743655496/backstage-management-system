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
        :type="isLightOn ? '' : 'info'"
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
          <el-dropdown-item
            icon="el-icon-close"
            @click.native="closeCurrentTag"
            :disabled="selectedTag?.fixed"
            >关闭</el-dropdown-item
          >
          <el-dropdown-item
            icon="el-icon-refresh-right"
            @click.native="$emit('refresh-view')"
            >重新加载</el-dropdown-item
          >
          <el-dropdown-item
            @click.native="toggleFixed(selectedTag)"
            :icon="selectedTag.fixed ? 'el-icon-unlock' : 'el-icon-lock'"
          >
            {{ selectedTag.fixed ? "取消固定" : "固定标签" }}
          </el-dropdown-item>
          <el-dropdown-item
            icon="iconfont icon-xinchuangkoudakai"
            @click.native="openInNewWindow"
            >在新窗口打开</el-dropdown-item
          >
          <el-dropdown-item
            icon="el-icon-d-arrow-left"
            divided
            @click.native="tabOperation('clearLeftAll')"
            >关闭左侧标签页</el-dropdown-item
          >
          <el-dropdown-item
            icon="el-icon-d-arrow-right"
            @click.native="tabOperation('clearRightAll')"
            >关闭右侧标签页</el-dropdown-item
          >
          <el-dropdown-item
            icon="iconfont icon-close-other"
            divided
            @click.native="tabOperation('clearOtherAll')"
            >关闭其他标签页</el-dropdown-item
          >
          <el-dropdown-item
            icon="iconfont icon-guanbiquanbu"
            @click.native="tabOperation('clearAll')"
            >关闭全部标签页</el-dropdown-item
          >
        </el-dropdown-menu>
      </el-dropdown>
      <button class="btn-tab" @click="$emit('fangda-suoxiao')">
        <i
          :class="
            isImmersive ? 'iconfont icon-suoxiao' : 'iconfont icon-fangda'
          "
        ></i>
      </button>
    </div>
  </el-row>
</template>

<script>
import navigation from "@/utils/navigation";
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  computed: {
    ...mapState("MenuStateModule", ["TabMenu"]),
    ...mapGetters("LightModule", [
      "backgroundColor",
      "textColor",
      "buttonHoverColor",
      "border_color",
      "tab_boder_color",
      "tab_background_color",
      "isLightOn",
    ]),
  },
  props: ["isImmersive"],
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
      "closeOtherTabs",
      "closeRightTabs",
      "closeLeftTabs",
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
    // 检查操控滚动按钮是否应该显现
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
    //标签页操作，关闭全部标签页
    tabOperation(type) {
      if (type === "clearAll") {
        this.clearTabMenu(this.$router);
      } else if (type === "clearOtherAll") {
        this.closeOtherTabs(this.$router);
      } else if (type === "clearLeftAll") {
        this.closeLeftTabs(this.$router);
      } else if (type === "clearRightAll") {
        this.closeRightTabs(this.$router);
      }
    },
    // 关闭标签
    handleCloseTag(tag, event) {
      event.stopPropagation(); // 阻止事件冒泡
      // 如果是当前激活的标签，需要特殊处理
      if (this.isActiveTag(tag)) {
        this.$store.dispatch("MenuStateModule/removeTabMenu", {
          path: tag.path,
          router: this.$router,
          if_current: true,
        });
      } else {
        this.$store.dispatch("MenuStateModule/removeTabMenu", {
          path: tag.path,
          router: this.$router,
          if_current: false,
        });
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
    // 操控是否固定
    toggleFixed(tag) {
      this.toggleFixedTabMenu(tag.path);
    },
    //在新窗口打开
    openInNewWindow() {
      if (!this.selectedTag || !this.selectedTag.path) return;
      const url = this.$router.resolve(this.selectedTag.path).href;
      window.open(url, "_blank");
    },
    //关闭当前标签
    closeCurrentTag() {
      if (!this.selectedTag || !this.selectedTag.path) return;

      this.$store.dispatch("MenuStateModule/removeTabMenu", {
        path: this.selectedTag.path,
        router: this.$router,
        if_current: this.isActiveTag(this.selectedTag),
      });
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
  border-left: none;
  border-top: 1px solid v-bind(border_color);
  border-bottom: 1px solid v-bind(border_color);
  border-right: none;
  display: flex;
  align-items: center;
  height: 34px;
  background-color: v-bind(backgroundColor);
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
      background-color: v-bind(tab_background_color);
      border: 1px solid v-bind(border_color);

      &.active {
        border-color: v-bind(tab_boder_color);
        color: v-bind(tab_boder_color);
        /deep/ .el-tag__close {
          color: v-bind(tab_boder_color); // 激活状态下的关闭按钮颜色
          &:hover {
            color: white;
          }
        }
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
      background-color: v-bind(backgroundColor);
      color: v-bind(textColor);
      border-left: 1px solid v-bind(border_color);
      border-top: none;
      border-bottom: none;
      border-right: none;

      cursor: pointer;
      font-size: 17px;
    }
    .btn-tab:hover {
      background-color: v-bind(buttonHoverColor);
    }
  }
}
</style>