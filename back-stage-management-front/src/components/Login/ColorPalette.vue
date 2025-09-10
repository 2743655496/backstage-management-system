<template>
  <div
    class="palette-container"
    @mouseenter="showPalette = true"
    @mouseleave="showPalette = false"
    @touchstart="showPalette = true"
    @touchend="showPalette = false"
  >
    <div class="palette-trigger" :style="{ color: currentColor }">
      <i class="iconfont icon-diaoseban"></i>
    </div>

    <transition name="slide">
      <div v-if="showPalette" class="palette-panel">
        <span
          v-for="color in colors"
          :key="color"
          class="color-dot"
          :style="{ backgroundColor: color }"
          @click="selectColor(color)"
        ></span>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "ColorPalette",
  props: {
    current_color: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showPalette: false,
      colors: [
        "#bddff5",
        "#f8b195",
        "#c5e1a5",
        "#ffccbc",
        "#90caf9",
        "#ffd54f",
        "#ce93d8",
      ],
    };
  },
  computed: {
    currentColor() {
      return this.current_color;
    },
  },
  methods: {
    selectColor(color) {
      this.$emit("select", color);
      this.showPalette = false;
    },
  },
};
</script>

<style scoped>
.palette-container {
  display: inline-block;
}

.palette-trigger {
  cursor: pointer;
}

.palette-panel {
  position: absolute;
  top: 0;
  left: -175px;
  display: flex;
  gap: 8px;
  background: #f2f2f2;
  padding: 10px;
  border-radius: 50px 0px 0px 50px;
  z-index: 10;
}

.color-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.color-dot:hover {
  transform: scale(1.2);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter,
.slide-leave-to {
  opacity: 0;
  transform: translateX(1px);
}
</style>
