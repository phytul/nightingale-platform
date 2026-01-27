<script setup lang="ts">
import { ref, onMounted } from "vue";
import TerminalWindow from "@/components/TerminalWindow.vue";
import { useRouter } from "vue-router";

const router = useRouter();

// 服务器监控数据
const serverStats = ref({
  totalServers: 12,
  onlineServers: 11,
  totalCpu: 45.2,
  totalMemory: 68.5,
  totalDisk: 52.3,
});

// 任务调度数据
const taskStats = ref({
  running: 8,
  completed: 1247,
  failed: 3,
  pending: 5,
});

// 大纲导航
const outlineItems = [
  { id: "intro", label: "平台介绍", icon: "mdi-information" },
  { id: "features", label: "功能栏", icon: "mdi-view-grid" },
  { id: "status", label: "状态栏", icon: "mdi-chart-box" },
];

// 大纲展开/收起状态
const isOutlineExpanded = ref(false);

// 切换大纲展开/收起
const toggleOutline = () => {
  isOutlineExpanded.value = !isOutlineExpanded.value;
};

// 平滑滚动到指定位置
const scrollToSection = (id: string) => {
  const element = document.getElementById(id);
  if (element) {
    const headerOffset = 80; // 考虑固定头部的高度
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

    window.scrollTo({
      top: offsetPosition,
      behavior: "smooth",
    });
  }
  // 点击后自动收起
  isOutlineExpanded.value = false;
};

// 模拟数据更新
onMounted(() => {
  // 可以在这里添加定时器来更新数据
  // setInterval(() => { ... }, 5000);
});
</script>

<template>
  <div class="home-container">
    <!-- 大纲导航 -->
    <div class="outline-nav" :class="{ expanded: isOutlineExpanded }">
      <button class="outline-toggle" @click="toggleOutline" :title="isOutlineExpanded ? '收起大纲' : '展开大纲'">
        <v-icon :icon="isOutlineExpanded ? 'mdi-chevron-right' : 'mdi-menu'" size="1rem"></v-icon>
      </button>
      <div v-if="isOutlineExpanded" class="outline-content">
        <div class="outline-header">
          <span class="prompt">$</span>
          <span class="command">cat outline.md</span>
        </div>
        <div class="outline-list">
          <button
            v-for="item in outlineItems"
            :key="item.id"
            class="outline-item"
            @click="scrollToSection(item.id)"
          >
            <v-icon :icon="item.icon" size="0.875rem"></v-icon>
            <span>{{ item.label }}</span>
          </button>
        </div>
      </div>
      <div v-else class="outline-icons">
        <button
          v-for="item in outlineItems"
          :key="item.id"
          class="outline-icon-item"
          @click="scrollToSection(item.id)"
          :title="item.label"
        >
          <v-icon :icon="item.icon" size="1rem"></v-icon>
        </button>
      </div>
    </div>

    <!-- 平台介绍和功能导航 -->
    <TerminalWindow title="cat /etc/motd && ls -la /usr/bin/nightingale/@nightingale:~" max-width="100%">
      <div class="intro-navigation-section">
        <!-- 介绍部分 -->
        <div id="intro" class="intro-section">
          <div class="command-line">
            <span class="prompt">$</span>
            <span class="command">cat /etc/motd</span>
          </div>
          <div class="output-text">
            <div class="welcome-banner">
              <span class="bracket">[</span> Nightingale Platform <span class="bracket">]</span>
            </div>
            <div class="info-line">
              <span class="symbol">></span>
              服务器监控及任务调度平台 · 提供实时监控、任务管理、性能分析等功能
            </div>
          </div>
        </div>

        <!-- 分隔线 -->
        <div class="section-divider"></div>

        <!-- 功能导航 -->
        <div id="features" class="navigation-section">
          <div class="command-line">
            <span class="prompt">$</span>
            <span class="command">ls -la /usr/bin/nightingale/</span>
          </div>
          <div class="output-text">
            <div class="info-line">
              <span class="symbol">></span>
              可用功能模块
            </div>
          </div>
          <div class="nav-grid">
          <button class="nav-card" @click="() => router.push('/servers')">
            <div class="nav-icon">
              <v-icon icon="mdi-server" size="2rem"></v-icon>
            </div>
            <div class="nav-content">
              <div class="nav-prompt">
                <span class="prompt">$</span>
                <span class="command-text">./servers.sh</span>
              </div>
              <div class="nav-title">服务器管理</div>
              <div class="nav-desc">查看和管理服务器列表</div>
            </div>
          </button>

          <button class="nav-card" @click="() => router.push('/monitoring')">
            <div class="nav-icon">
              <v-icon icon="mdi-chart-line" size="2rem"></v-icon>
            </div>
            <div class="nav-content">
              <div class="nav-prompt">
                <span class="prompt">$</span>
                <span class="command-text">./monitoring.sh</span>
              </div>
              <div class="nav-title">实时监控</div>
              <div class="nav-desc">查看服务器实时性能指标</div>
            </div>
          </button>

          <button class="nav-card" @click="() => router.push('/tasks')">
            <div class="nav-icon">
              <v-icon icon="mdi-play-circle" size="2rem"></v-icon>
            </div>
            <div class="nav-content">
              <div class="nav-prompt">
                <span class="prompt">$</span>
                <span class="command-text">./tasks.sh</span>
              </div>
              <div class="nav-title">任务调度</div>
              <div class="nav-desc">创建和管理定时任务</div>
            </div>
          </button>

          <button class="nav-card" @click="() => router.push('/logs')">
            <div class="nav-icon">
              <v-icon icon="mdi-file-document" size="2rem"></v-icon>
            </div>
            <div class="nav-content">
              <div class="nav-prompt">
                <span class="prompt">$</span>
                <span class="command-text">./logs.sh</span>
              </div>
              <div class="nav-title">日志查看</div>
              <div class="nav-desc">查看系统和服务日志</div>
            </div>
          </button>

          <button class="nav-card" @click="() => router.push('/alerts')">
            <div class="nav-icon">
              <v-icon icon="mdi-bell" size="2rem"></v-icon>
            </div>
            <div class="nav-content">
              <div class="nav-prompt">
                <span class="prompt">$</span>
                <span class="command-text">./alerts.sh</span>
              </div>
              <div class="nav-title">告警管理</div>
              <div class="nav-desc">配置和管理系统告警</div>
            </div>
          </button>

          <button class="nav-card" @click="() => router.push('/settings')">
            <div class="nav-icon">
              <v-icon icon="mdi-cog" size="2rem"></v-icon>
            </div>
            <div class="nav-content">
              <div class="nav-prompt">
                <span class="prompt">$</span>
                <span class="command-text">./settings.sh</span>
              </div>
              <div class="nav-title">系统设置</div>
              <div class="nav-desc">配置平台参数和选项</div>
            </div>
          </button>
          </div>
        </div>
      </div>
    </TerminalWindow>

    <!-- 数据概览 -->
    <div id="status" class="stats-grid">
      <!-- 服务器监控数据 -->
      <TerminalWindow title="server-monitor@nightingale:~" max-width="100%">
        <div class="stats-section">
          <div class="command-line">
            <span class="prompt">$</span>
            <span class="command">./server-monitor.sh --status</span>
          </div>
          <div class="stats-content">
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                服务器总数
              </div>
              <div class="stat-value">{{ serverStats.totalServers }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                在线服务器
              </div>
              <div class="stat-value online">{{ serverStats.onlineServers }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                CPU 使用率
              </div>
              <div class="stat-value">{{ serverStats.totalCpu }}%</div>
              <div class="stat-bar">
                <div
                  class="stat-bar-fill cpu"
                  :style="{ width: `${serverStats.totalCpu}%` }"
                ></div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                内存使用率
              </div>
              <div class="stat-value">{{ serverStats.totalMemory }}%</div>
              <div class="stat-bar">
                <div
                  class="stat-bar-fill memory"
                  :style="{ width: `${serverStats.totalMemory}%` }"
                ></div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                磁盘使用率
              </div>
              <div class="stat-value">{{ serverStats.totalDisk }}%</div>
              <div class="stat-bar">
                <div
                  class="stat-bar-fill disk"
                  :style="{ width: `${serverStats.totalDisk}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </TerminalWindow>

      <!-- 任务调度数据 -->
      <TerminalWindow title="task-scheduler@nightingale:~" max-width="100%">
        <div class="stats-section">
          <div class="command-line">
            <span class="prompt">$</span>
            <span class="command">./task-scheduler.sh --stats</span>
          </div>
          <div class="stats-content">
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                运行中
              </div>
              <div class="stat-value running">{{ taskStats.running }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                已完成
              </div>
              <div class="stat-value completed">{{ taskStats.completed }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                失败
              </div>
              <div class="stat-value failed">{{ taskStats.failed }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">
                <span class="symbol">></span>
                等待中
              </div>
              <div class="stat-value pending">{{ taskStats.pending }}</div>
            </div>
          </div>
        </div>
      </TerminalWindow>
    </div>
  </div>
</template>

<style scoped lang="scss">
.home-container {
  display: flex;
  flex-direction: column;
  gap: calc($space * 8);
  padding-bottom: calc($space * 8);
  position: relative;
}

.outline-nav {
  position: fixed;
  right: 0;
  top: calc(50% + calc($space * 8));
  transform: translateY(-50%);
  z-index: 40;
  background-color: color-mix(in srgb, $background 92%, $form-card-bg-mix);
  border: 3px solid color-mix(in srgb, $border-color 100%, $form-card-border-mix);
  border-right: none;
  border-radius: 6px 0 0 6px;
  padding: calc($space * 3);
  width: 48px;
  outline: 1px solid color-mix(in srgb, $border-color 30%, transparent);
  outline-offset: 2px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: calc($space * 2);

  &.expanded {
    width: 180px;
    padding: calc($space * 4);
  }

  .outline-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    background-color: color-mix(in oklab, $green-500 10%, transparent);
    border: 1px solid color-mix(in srgb, $green-500 30%, transparent);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: $green-500;
    flex-shrink: 0;

    &:hover {
      background-color: color-mix(in oklab, $green-500 20%, transparent);
      border-color: color-mix(in srgb, $green-500 50%, transparent);
      transform: scale(1.05);
    }

    :deep(.v-icon) {
      color: $green-500;
    }
  }

  .outline-icons {
    display: flex;
    flex-direction: column;
    gap: calc($space * 2);
  }

  .outline-icon-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    background-color: transparent;
    border: 1px solid color-mix(in srgb, $border-color 30%, transparent);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: $muted-foreground;

    &:hover {
      background-color: color-mix(in oklab, $green-500 15%, transparent);
      border-color: color-mix(in srgb, $green-500 50%, transparent);
      color: $green-500;
      transform: scale(1.1);
    }

    :deep(.v-icon) {
      color: inherit;
    }
  }

  .outline-content {
    display: flex;
    flex-direction: column;
    gap: calc($space * 2);
    animation: fadeIn 0.2s ease;
  }

  .outline-header {
    display: flex;
    align-items: center;
    gap: calc($space * 2);
    margin-bottom: calc($space * 2);
    padding-bottom: calc($space * 4);
    border-bottom: 1px dashed $form-card-border-mix-result;
    font-size: 0.75rem;
    font-family: $font-mono;

    .prompt {
      color: $green-500;
      font-weight: 600;
    }

    .command {
      color: $foreground;
    }
  }

  .outline-list {
    display: flex;
    flex-direction: column;
    gap: calc($space * 2);
  }

  .outline-item {
    display: flex;
    align-items: center;
    gap: calc($space * 3);
    padding: calc($space * 3) calc($space * 4);
    background-color: transparent;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: $muted-foreground;
    font-size: 0.75rem;
    font-family: $font-mono;
    text-align: left;
    width: 100%;

    &:hover {
      background-color: color-mix(in oklab, $green-500 15%, transparent);
      color: $foreground;
      transform: translateX(4px);

      :deep(.v-icon) {
        color: $green-500;
      }
    }

    :deep(.v-icon) {
      color: $muted-foreground;
      transition: color 0.2s ease;
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

// 响应式：在小屏幕上隐藏大纲导航
@media (max-width: 1024px) {
  .outline-nav {
    display: none;
  }
}

.intro-navigation-section {
  display: flex;
  flex-direction: column;
  gap: calc($space * 6);
}

.intro-section {
  scroll-margin-top: calc($space * 20);

  .command-line {
    display: flex;
    align-items: center;
    gap: calc($space * 2);
    margin-bottom: calc($space * 2);
    font-size: 0.875rem;
  }

  .prompt {
    color: $green-500;
    font-weight: 600;
    font-family: $font-mono;
  }

  .command {
    color: $foreground;
    font-family: $font-mono;
  }

  .output-text {
    padding-left: calc($space * 6);
    font-size: 0.875rem;
    line-height: 1.5;
  }

  .welcome-banner {
    margin-bottom: calc($space * 2);
    color: $foreground;
    font-weight: 500;
    font-size: 0.875rem;

    .bracket {
      color: $green-500;
      font-weight: 600;
    }
  }

  .info-line {
    color: $muted-foreground;
    font-family: $font-mono;
    font-size: 0.75rem;
    line-height: 1.5;

    .symbol {
      color: $green-500;
      margin-right: calc($space * 2);
    }
  }
}

.section-divider {
  height: 1px;
  background: $form-card-border-mix-result;
  margin: calc($space * 4) 0;
  border: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: calc($space * 8);
  scroll-margin-top: calc($space * 20);
}

.stats-section {
  .command-line {
    display: flex;
    align-items: center;
    gap: calc($space * 2);
    margin-bottom: calc($space * 6);
    font-size: 0.875rem;
    padding-bottom: calc($space * 4);
    border-bottom: 1px dashed $form-card-border-mix-result;
  }

  .prompt {
    color: $green-500;
    font-weight: 600;
    font-family: $font-mono;
  }

  .command {
    color: $foreground;
    font-family: $font-mono;
  }

  .stats-content {
    display: flex;
    flex-direction: column;
    gap: calc($space * 6);
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    gap: calc($space * 2);
  }

  .stat-label {
    display: flex;
    align-items: center;
    gap: calc($space * 2);
    color: $muted-foreground;
    font-family: $font-mono;
    font-size: 0.75rem;

    .symbol {
      color: $green-500;
    }
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: $foreground;
    font-family: $font-mono;

    &.online {
      color: $green-500;
    }

    &.running {
      color: $green-500;
    }

    &.completed {
      color: $green-500;
    }

    &.failed {
      color: #ff5f57;
    }

    &.pending {
      color: #ffbd2e;
    }
  }

  .stat-bar {
    width: 100%;
    height: 8px;
    background-color: color-mix(in srgb, $border-color 20%, transparent);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
  }

  .stat-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
    position: relative;

    &.cpu {
      background: linear-gradient(
        90deg,
        color-mix(in oklab, $green-500 80%, transparent),
        $green-500
      );
    }

    &.memory {
      background: linear-gradient(
        90deg,
        color-mix(in oklab, #3b82f6 80%, transparent),
        #3b82f6
      );
    }

    &.disk {
      background: linear-gradient(
        90deg,
        color-mix(in oklab, #8b5cf6 80%, transparent),
        #8b5cf6
      );
    }

    &::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(
        90deg,
        transparent,
        color-mix(in oklab, white 20%, transparent),
        transparent
      );
      animation: shimmer 2s infinite;
    }
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.navigation-section {
  scroll-margin-top: calc($space * 20);

  .command-line {
    display: flex;
    align-items: center;
    gap: calc($space * 2);
    margin-bottom: calc($space * 2);
    font-size: 0.875rem;
  }

  .prompt {
    color: $green-500;
    font-weight: 600;
    font-family: $font-mono;
  }

  .command {
    color: $foreground;
    font-family: $font-mono;
  }

  .output-text {
    padding-left: calc($space * 6);
    margin-bottom: calc($space * 6);
  }

  .info-line {
    color: $muted-foreground;
    font-family: $font-mono;
    font-size: 0.875rem;

    .symbol {
      color: $green-500;
      margin-right: calc($space * 2);
    }
  }

  .nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: calc($space * 6);
  }

  .nav-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc($space * 4);
    padding: calc($space * 8);
    background-color: color-mix(in srgb, $background 100%, $form-card-bg-mix);
    border: 1px solid color-mix(in srgb, $border-color 20%, $form-card-border-mix);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
    position: relative;
    overflow: hidden;

    &::before {
      content: "";
      position: absolute;
      inset: 0;
      border-radius: 4px;
      padding: 1px;
      background: conic-gradient(
        from 0deg,
        transparent 0deg,
        color-mix(in oklab, $green-500 30%, transparent) 60deg,
        transparent 120deg,
        color-mix(in oklab, $green-500 30%, transparent) 180deg,
        transparent 240deg,
        transparent 360deg
      );
      -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
      mask-composite: exclude;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    &:hover {
      border-color: color-mix(in oklab, $green-500 50%, transparent);
      background-color: color-mix(in oklab, $green-500 5%, transparent);
      transform: translateY(-2px);
      box-shadow:
        0 4px 12px color-mix(in oklab, $green-500 5%, transparent),
        0 2px 4px color-mix(in oklab, $shadow-color 10%, transparent);

      &::before {
        opacity: 1;
        animation: border-gradient-flow 3s linear infinite;
      }

      .nav-prompt .command-text {
        color: $green-500;
      }

      .nav-icon {
        transform: scale(1.1);
        color: $green-500;
      }
    }

    &:active {
      transform: translateY(0);
    }
  }

  .nav-icon {
    color: $muted-foreground;
    transition: all 0.2s ease;
  }

  .nav-content {
    display: flex;
    flex-direction: column;
    gap: calc($space * 3);
    width: 100%;
  }

  .nav-prompt {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: calc($space * 2);
    font-family: $font-mono;
    font-size: 0.75rem;

    .prompt {
      color: $green-500;
      font-weight: 600;
    }

    .command-text {
      color: $muted-foreground;
      transition: color 0.2s ease;
    }
  }

  .nav-title {
    font-size: 1rem;
    font-weight: 600;
    color: $foreground;
    margin-top: calc($space * 2);
  }

  .nav-desc {
    font-size: 0.75rem;
    color: $muted-foreground;
    line-height: 1.5;
  }
}

@keyframes border-gradient-flow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .nav-grid {
    grid-template-columns: 1fr;
  }
}
</style>