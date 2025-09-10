<template>
  <div
    class="slider-container"
    ref="container"
    @touchstart="startDrag"
    @mousedown="startDrag"
  >
    <div
      class="slider-track"
      :style="{ width: trackWidth + 'px', backgroundColor: trackColor }"
    ></div>
    <div
      class="slider-button"
      :style="{ left: buttonLeft + 'px', backgroundColor: buttonColor }"
    >
      <span v-if="!isPassed"><i class="el-icon-d-arrow-right"></i></span>
      <span v-else><i class="el-icon-check"></i></span>
    </div>
    <div class="slider-text" v-if="!isPassed">{{ text }}</div>
    <div class="slider-text2" v-else>{{ successText }}</div>
  </div>
</template>

<script>
export default {
  name: "SliderVerify",
  props: {
    height: { type: Number, default: 40 },
    text: { type: String, default: "请将滑块拖动到右侧" },
    successText: { type: String, default: "验证成功" },
    trackColor: { type: String, default: "#4caf50" },
    buttonColor: { type: String, default: "#fff" },
  },
  data() {
    return {
      isDragging: false,
      startX: 0,
      buttonLeft: 0,
      trackWidth: 0,
      isPassed: false,
      containerWidth: 0,
      dragTrail: [], // 👈 拖动轨迹记录
    };
  },
  mounted() {
    this.resizeObserver = new ResizeObserver(() => {
      this.updateContainerWidth();
    });
    this.resizeObserver.observe(this.$refs.container);
  },
  beforeDestroy() {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
  },

  methods: {
    resetSlider() {
      this.isPassed = false;
      this.buttonLeft = 0;
      this.trackWidth = 0;
      this.dragTrail = [];
    },
    analyzeTrail(trail) {
      if (trail.length < 6) return false; // 太少点，可能是模拟

      const duration = trail[trail.length - 1].time - trail[0].time;

      // 快速拖动也可以接受，但必须有足够抖动
      const jitterCount = trail.reduce((count, point, i, arr) => {
        if (i === 0) return count;
        const dx = Math.abs(point.x - arr[i - 1].x);
        return dx > 2 ? count + 1 : count;
      }, 0);

      const jitterRatio = jitterCount / trail.length;

      if (duration < 250 && jitterRatio < 0.3) return false; // 快且太平滑，拒绝
      if (duration >= 250 || jitterRatio >= 0.3) return true; // 满足任一条件即可通过

      return false;
    },

    updateContainerWidth() {
      this.$nextTick(() => {
        if (this.$refs.container) {
          this.containerWidth = this.$refs.container.offsetWidth;

          // 如果已经验证通过，重新设置滑块位置
          if (this.isPassed) {
            const maxX = this.containerWidth - this.height;
            this.buttonLeft = maxX;
            this.trackWidth = maxX + this.height;
          }
        }
      });
    },

    startDrag(e) {
      if (this.isPassed) return;
      this.isDragging = true;
      this.startX = (e.clientX || e.touches[0].clientX) - this.buttonLeft;
      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.endDrag);
      document.addEventListener("touchmove", this.onDrag);
      document.addEventListener("touchend", this.endDrag);
    },
    onDrag(e) {
      if (!this.isDragging) return;
      const clientX = e.clientX || e.touches[0].clientX;
      const timestamp = Date.now();
      let moveX = clientX - this.startX;
      const maxX = this.containerWidth - this.height;
      moveX = Math.max(0, Math.min(moveX, maxX));

      // 👣 记录轨迹点
      this.dragTrail.push({ x: moveX, time: timestamp });

      this.buttonLeft = moveX;
      this.trackWidth = moveX + this.height;
    },
    endDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.endDrag);
      document.removeEventListener("touchmove", this.onDrag);
      document.removeEventListener("touchend", this.endDrag);

      const maxX = this.containerWidth - this.height;

      // 🧠 分析轨迹
      const isHumanLike = this.analyzeTrail(this.dragTrail);

      if (this.buttonLeft >= maxX - 5 && isHumanLike) {
        this.isPassed = true;
        this.$emit("pass", this.dragTrail);
      } else {
        this.buttonLeft = 0;
        this.trackWidth = 0;
        this.dragTrail = []; // 清空轨迹
      }
    },
  },
};
</script>

<style scoped>
.slider-container {
  position: relative;
  width: 100%;
  max-width: 450px;
  height: 40px;
  background: #d3d3d3;
  border-radius: 4px;
  user-select: none;
  overflow: hidden;
}
.slider-track {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  /* transition: width 0.2s; */
  border-radius: 4px;
}
.slider-button {
  position: absolute;
  top: 0;
  width: 40px;
  height: 100%;
  text-align: center;
  line-height: 40px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  z-index: 2;
  touch-action: none;
}
.slider-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  line-height: 40px;
  text-align: center;
  font-size: 14px;
  z-index: 1;
  font-family: "Microsoft YaHei", sans-serif;
  font-weight: bold;
  background: linear-gradient(
    90deg,
    #606266 0%,
    #fff 20%,
    #606266 40%,
    #606266 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 2s linear infinite;
}
.slider-text2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  line-height: 40px;
  text-align: center;
  font-size: 14px;
  color: #ffffff;
}
@keyframes shine {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 100% 0;
  }
}
</style>
