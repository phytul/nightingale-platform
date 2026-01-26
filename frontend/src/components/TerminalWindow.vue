<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

interface Props {
  title?: string;
  maxWidth?: string;
}

withDefaults(defineProps<Props>(), {
  title: "terminal@nightingale:~",
  maxWidth: "480px",
});

const terminalWindow = ref<HTMLElement | null>(null);
const rotateX = ref(0);
const rotateY = ref(0);

const handleMouseMove = (e: MouseEvent) => {
  if (!terminalWindow.value) return;

  const rect = terminalWindow.value.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;

  const mouseX = e.clientX - centerX;
  const mouseY = e.clientY - centerY;

  // 计算倾斜角度，最大角度为 5 度
  const maxRotate = 5;
  rotateY.value = (mouseX / (rect.width / 2)) * maxRotate;
  rotateX.value = -(mouseY / (rect.height / 2)) * maxRotate;
};

const handleMouseLeave = () => {
  rotateX.value = 0;
  rotateY.value = 0;
};

onMounted(() => {
  if (terminalWindow.value) {
    terminalWindow.value.addEventListener("mousemove", handleMouseMove);
    terminalWindow.value.addEventListener("mouseleave", handleMouseLeave);
  }
});

onUnmounted(() => {
  if (terminalWindow.value) {
    terminalWindow.value.removeEventListener("mousemove", handleMouseMove);
    terminalWindow.value.removeEventListener("mouseleave", handleMouseLeave);
  }
});
</script>

<template>
  <div
    ref="terminalWindow"
    class="terminal-window"
    :style="{
      transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
      maxWidth: maxWidth,
    }"
  >
    <!-- 终端标题栏 -->
    <div class="terminal-header">
      <div class="terminal-controls">
        <span class="control-dot red"></span>
        <span class="control-dot yellow"></span>
        <span class="control-dot green"></span>
      </div>
      <div class="terminal-title">{{ title }}</div>
      <div class="terminal-spacer"></div>
    </div>

    <!-- 终端内容区 -->
    <div class="terminal-body">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="scss">
.terminal-window {
  width: 100%;
  background-color: $background;
  border-radius: 8px;
  border: 1px solid $form-card-border-mix-result;
  box-shadow:
    0 4px 6px -1px color-mix(in srgb, $shadow-color 10%, transparent),
    0 2px 4px -1px color-mix(in srgb, $shadow-color 6%, transparent),
    0 0 0 1px $terminal-window-border,
    0 20px 25px -5px color-mix(in srgb, $shadow-color 10%, transparent),
    0 10px 10px -5px color-mix(in srgb, $shadow-color 4%, transparent);
  overflow: hidden;
  font-family: $font-mono;
  transition:
    border-color 0.3s ease,
    box-shadow 0.3s ease,
    transform 0.1s ease-out;
  transform-style: preserve-3d;

  &:hover {
    border-color: color-mix(in oklab, $color-primary 50%, transparent);
    box-shadow:
      0 4px 6px -1px color-mix(in srgb, $shadow-color 10%, transparent),
      0 2px 4px -1px color-mix(in srgb, $shadow-color 6%, transparent),
      0 0 0 1px color-mix(in oklab, $color-primary 50%, transparent),
      0 0 0 2px color-mix(in srgb, $color-primary 20%, transparent),
      0 20px 25px -5px color-mix(in srgb, $shadow-color 10%, transparent),
      0 10px 10px -5px color-mix(in srgb, $shadow-color 4%, transparent),
      0 0 30px color-mix(in srgb, $color-primary 15%, transparent);
  }
}

.terminal-header {
  display: flex;
  align-items: center;
  padding: calc($space * 4) calc($space * 6);
  background: linear-gradient(to bottom, $header-gradient-start, $header-gradient-end);
  border-bottom: 1px solid color-mix(in srgb, rgb(var(--v-theme-border)) 50%, transparent);
  gap: calc($space * 4);
}

.terminal-controls {
  display: flex;
  gap: calc($space * 2);
  align-items: center;
}

.control-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);

  &.red {
    background-color: #ff5f57;
  }

  &.yellow {
    background-color: #ffbd2e;
  }

  &.green {
    background-color: #28ca42;
  }
}

.terminal-title {
  flex: 1;
  font-size: 0.75rem;
  color: $muted-foreground;
  text-align: center;
  font-family: $font-mono;
  letter-spacing: 0.5px;
}

.terminal-spacer {
  width: 60px;
}

.terminal-body {
  padding: calc($space * 8) calc($space * 10);
  min-height: 320px;
}
</style>
