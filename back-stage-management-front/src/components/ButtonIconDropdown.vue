<template>
  <div class="icon-dropdown" ref="dropdown">
    <!-- 图标按钮 -->
    <button class="btn-radius" @click.stop="handleIconClick">
      <i :class="['trigger-icon', triggerIconClass, { active: isOpen }]"></i>
    </button>
    <!-- 下拉菜单带动画 -->
    <transition name="fade-slide">
      <ul v-if="isOpen" class="dropdown-menu">
        <li
          v-for="item in iconList"
          :key="item.icon"
          @click="selectIcon(item)"
          :class="{ selected: item.icon === localSelectedIcon }"
        >
          <i :class="item.icon"></i>
          <span>{{ item.name }}</span>
        </li>
      </ul>
    </transition>
  </div>
</template>

<script>
export default {
  name: "IconDropdown",
  props: {
    iconList: {
      type: Array,
      required: true,
    },
    triggerIconClass: {
      type: String,
      required: true,
    },
    backgroundColor: {
      type: String,
      default: "white",
    },
    textColor: {
      type: String,
      default: "#000000",
    },
    hoverColor: {
      type: String,
      default: "#f5f5f5",
    },
    selectedIcon: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
      localSelectedIcon: this.selectedIcon, // 本地副本
    };
  },
  watch: {
    selectedIcon(newVal) {
      this.localSelectedIcon = newVal;
    },
  },
  mounted() {
    window.addEventListener("blur", this.handleWindowBlur);
  },
  beforeDestroy() {
    window.removeEventListener("blur", this.handleWindowBlur);
  },
  methods: {
    handleWindowBlur() {
      this.closeDropdown();
    },
    closeDropdown() {
      this.isOpen = false;
      document.removeEventListener("click", this.handleClickOutside, true);
    },
    handleIconClick() {
      this.isOpen = true;
      setTimeout(() => {
        document.addEventListener("click", this.handleClickOutside, true);
      }, 0);
    },
    selectIcon(item) {
      this.localSelectedIcon = item.icon;
      this.$emit("select", item); // 向父组件发送选中事件
      this.closeDropdown();
    },
    handleClickOutside(event) {
      if (!this.$refs.dropdown.contains(event.target)) {
        this.closeDropdown();
      }
    },
  },
};
</script>

<style scoped>
.btn-radius {
  margin-left: 4px;
  padding: 8px 8px;
  background-color: v-bind(backgroundColor);
  color: v-bind(textColor);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 17px;
}
.btn-radius:hover {
  background-color: v-bind(hoverColor);
}
.trigger-icon {
  cursor: pointer;
  transition: color 0.3s ease, transform 0.3s ease;
}
/* .trigger-icon:hover {
  color: #1890ff;
} */
/* .trigger-icon.active {
  color: #1890ff;
  transform: rotate(90deg);
} */

.dropdown-menu {
  position: absolute;
  margin-top: 8px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  list-style: none;
  padding: 6px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 4;
}
.dropdown-menu li {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.dropdown-menu li:hover {
  background-color: #f5f5f5;
}
.dropdown-menu li.selected {
  background-color: #e6f7ff;
}
.dropdown-menu li i {
  margin-right: 8px;
}

/* 动画过渡效果 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
