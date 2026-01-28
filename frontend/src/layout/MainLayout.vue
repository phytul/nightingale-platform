<script setup lang="ts">
import useCustomTheme from "@/hooks/useCustomTheme";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const customTheme = useCustomTheme();

const menuItems = [
  { name: "服务器管理", path: "/servers", icon: "mdi-server" },
  { name: "任务调度", path: "/tasks", icon: "mdi-calendar-clock" },
  { name: "系统设置", path: "/settings", icon: "mdi-cog" },
];

const isActive = (path: string) => {
  return route.path === path;
};
</script>

<template>
  <div class="header">
    <div class="header-container">
      <div class="main-title" @click="router.push('/home')">
        <div class="status-tag">
          <span class="ready">ready</span>
        </div>
        <div class="page-title">
          <span class="path-prefix">~/</span>
          <span class="title-text">Nightingale</span>
          <span class="cursor-blink"></span>
        </div>
      </div>
      <nav class="header-nav">
        <div class="nav-menu">
          <button
            v-for="item in menuItems"
            :key="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
            @click="router.push(item.path)"
          >
            <v-icon size="1rem" :icon="item.icon"></v-icon>
            <span class="nav-text">{{ item.name }}</span>
          </button>
        </div>
      </nav>
      <div class="header-right">
        <v-btn @click="customTheme.toggle()"
          ><v-icon
            size="1.125rem"
            icon="mdi mdi-weather-sunny"
            v-if="customTheme.currentTheme === 'customLightTheme'"
          ></v-icon>
          <v-icon
            size="1rem"
            icon="mdi mdi-weather-night"
            v-if="customTheme.currentTheme === 'customDarkTheme'"
          ></v-icon
        ></v-btn>
        <v-btn @click="router.push('/login')">
          <div class="btn-container">
            <span class="sign">$</span> <span>登录</span>
            <v-icon size="1rem" class="mdi mdi-login"></v-icon></div
        ></v-btn>
      </div>
    </div>
  </div>

  <div class="main-container">
    <RouterView />
  </div>
</template>

<style scoped lang="scss">
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background-color: color-mix(in srgb, $background 95%, transparent);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid $form-card-border-mix-result;
  box-shadow: 0 1px 3px color-mix(in srgb, $shadow-color 5%, transparent);
  transition: box-shadow 0.3s ease, background-color 0.3s ease;

  .header-container {
    display: flex;
    height: calc($space * 16);
    max-width: $container-7xl;
    margin: 0 auto;
    padding-inline: calc($space * 8);
    justify-content: space-between;
    align-items: center;
    gap: calc($space * 4);
    flex-wrap: nowrap;

    .main-title {
      display: flex;
      gap: calc($space * 4);
      align-items: center;
      cursor: pointer;
      transition: opacity 0.2s ease;
      flex-shrink: 0;
      min-width: 0;

      &:hover {
        opacity: 0.8;
      }

      .status-tag {
        display: flex;
        gap: calc($space * 2);
        align-items: center;
        padding-top: calc($space * 1.5);
        padding-bottom: calc($space * 1.8);
        padding-inline: calc($space * 3);
        border: 1px solid $form-card-border-mix-result;
        border-radius: $radius;
        color: $muted-foreground;
        font-size: $text-xm;
        background-color: $muted-color;
        font-family: $font-mono;
        transition: all 0.2s ease;
        cursor: pointer;
        box-sizing: border-box;
        flex-shrink: 0;

        &::before {
          display: block;
          content: "";
          width: calc($space * 2);
          height: calc($space * 2);
          background-color: color-mix(in oklab, $green-500 80%, transparent);
          border-radius: 50%;
          transition: all 0.2s ease;
        }

        .ready {
          transition: all 0.2s ease;
        }

        &:hover {
          border-color: color-mix(in srgb, $color-primary 50%, transparent);
          background-color: color-mix(in srgb, $muted-color 80%, $color-primary 20%);
          transform: translateY(-1px);
          box-shadow: 0 2px 8px color-mix(in srgb, $color-primary 20%, transparent);

          .ready {
            color: $color-primary;
          }

          &::before {
            background-color: color-mix(in oklab, $green-500 100%, transparent);
            transform: scale(1.1);
          }
        }
      }

      .page-title {
        display: flex;
        align-items: center;
        font-family: $font-mono;
        font-size: $text-xl;
        color: $foreground;
        gap: calc($space * 1);
        font-weight: bold;
        min-width: 0;
        overflow: hidden;

        .path-prefix {
          color: $color-primary;
        }

        .title-text {
          color: $foreground;
        }

        .cursor-blink {
          display: inline-block;
          width: 2px;
          height: 1em;
          background-color: $color-primary;
          margin-left: calc($space * 1);
          animation: blink 1s infinite;
        }
      }
    }

    .header-nav {
      flex: 1;
      display: flex;
      justify-content: center;
      min-width: 0;
      overflow: hidden;

      .nav-menu {
        display: flex;
        gap: calc($space * 1);
        align-items: center;
        flex-wrap: nowrap;
        justify-content: center;
        overflow-x: auto;
        scrollbar-width: none;
        -ms-overflow-style: none;

        &::-webkit-scrollbar {
          display: none;
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: calc($space * 1.5);
          padding: calc($space * 2) calc($space * 3);
          border: 1px solid transparent;
          border-radius: $radius;
          background-color: transparent;
          color: $muted-foreground;
          font-size: $text-sm;
          font-family: $font-mono;
          cursor: pointer;
          transition: all 0.2s ease;
          white-space: nowrap;
          min-height: calc($space * 8);
          flex-shrink: 0;

          &:hover {
            background-color: color-mix(in srgb, $muted-color 80%, transparent);
            border-color: color-mix(in srgb, $form-card-border-mix-result 50%, transparent);
            color: $foreground;
          }

          &.active {
            background-color: color-mix(in srgb, $color-primary 10%, transparent);
            border-color: color-mix(in srgb, $color-primary 30%, transparent);
            color: $color-primary;
            font-weight: 500;

            &:hover {
              background-color: color-mix(in srgb, $color-primary 15%, transparent);
              border-color: color-mix(in srgb, $color-primary 40%, transparent);
            }
          }

          .nav-text {
            @media (max-width: 768px) {
              display: none;
            }
          }

          :deep(.v-icon) {
            flex-shrink: 0;
          }
        }
      }
    }

    .header-right {
      display: flex;
      gap: calc($space * 4);
      align-items: center;
      flex-shrink: 0;

      .btn-container {
        display: flex;
        gap: $space;
      }

      .sign {
        color: $green-500;
      }
    }

    @media (max-width: 1024px) {
      padding-inline: calc($space * 4);
      gap: calc($space * 2);

      .main-title {
        gap: calc($space * 2);

        .page-title {
          font-size: $text-xm;
        }

        .status-tag {
          padding-inline: calc($space * 2);
          font-size: $text-xs;
        }
      }

      .header-nav .nav-menu {
        gap: calc($space * 1);

        .nav-item {
          padding: calc($space * 2) calc($space * 2.5);
          font-size: $text-xs;
        }
      }
    }

    @media (max-width: 768px) {
      padding-inline: calc($space * 2);
      gap: calc($space * 2);
      height: auto;
      min-height: calc($space * 16);
      padding-block: calc($space * 2);
      flex-wrap: wrap;

      .main-title {
        flex: 1 1 auto;
        min-width: 0;

        .page-title {
          font-size: $text-xm;

          .title-text {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }
        }

        .status-tag {
          display: none;
        }
      }

      .header-nav {
        order: 3;
        width: 100%;
        flex: 1 1 100%;
        padding-top: calc($space * 3);
        position: relative;

        &::before {
          content: "";
          position: absolute;
          top: 0;
          left: calc($space * -2);
          right: calc($space * -2);
          height: 1px;
          background: linear-gradient(
            to right,
            transparent,
            color-mix(in srgb, $form-card-border-mix-result 60%, transparent) 20%,
            color-mix(in srgb, $form-card-border-mix-result 60%, transparent) 80%,
            transparent
          );
        }

        .nav-menu {
          width: 100%;
          justify-content: space-between;
          gap: calc($space * 1);
          padding-block: calc($space * 2);
          background-color: color-mix(in srgb, $muted-color 30%, transparent);
          border-radius: $radius;
          padding-inline: calc($space * 2);

          .nav-item {
            flex: 1;
            justify-content: center;
            padding: calc($space * 2);
            min-width: 0;
          }
        }
      }

      .header-right {
        gap: calc($space * 2);
      }
    }

    @media (max-width: 480px) {
      padding-inline: calc($space * 1);

      .main-title .page-title {
        font-size: $text-sm;
      }

      .header-nav .nav-menu .nav-item {
        padding: calc($space * 1.5) calc($space * 1);
        font-size: $text-xs;

        :deep(.v-icon) {
          font-size: 0.875rem;
        }
      }
    }
  }
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}

.main-container {
  max-width: $container-7xl;
  margin: 0 auto;
  padding-block: calc($space * 4);
  padding-inline: calc($space * 8);
  background-color: $background;
  background-image:
    linear-gradient(color-mix(in srgb, $border-color 8%, transparent) 1px, transparent 1px),
    linear-gradient(90deg, color-mix(in srgb, $border-color 8%, transparent) 1px, transparent 1px);
  background-size: 24px 24px;
  background-position:
    0 0,
    0 0;
  background-repeat: repeat;
  min-height: calc(100vh - calc($space * 16));
}
</style>
