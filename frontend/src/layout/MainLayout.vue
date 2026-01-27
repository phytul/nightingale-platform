<script setup lang="ts">
import useCustomTheme from "@/hooks/useCustomTheme";
import { useRouter } from "vue-router";

const router = useRouter();

const customTheme = useCustomTheme();
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

    .main-title {
      display: flex;
      gap: calc($space * 4);
      align-items: center;
      cursor: pointer;
      transition: opacity 0.2s ease;

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

    .header-right {
      display: flex;
      gap: calc($space * 4);
      align-items: center;

      .btn-container {
        display: flex;
        gap: $space;
      }

      .sign {
        color: $green-500;
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
