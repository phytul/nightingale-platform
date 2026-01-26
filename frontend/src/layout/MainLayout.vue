<script setup lang="ts">
import useCustomTheme from "@/hooks/useCustomTheme";
import { useRouter } from "vue-router";

const router = useRouter();
const customTheme = useCustomTheme();
</script>

<template>
  <div class="header">
    <div class="header-container">
      <div class="header-left">
        <div class="status-tag">
          <span class="ready">ready</span>
        </div>
        <div class="main-title"></div>
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
  z-index: 50;
  border-bottom: 1px solid $form-card-border-mix-result;

  .header-container {
    display: flex;
    height: calc($space * 16);
    max-width: $container-7xl;
    margin: 0 auto;
    padding-inline: calc($space * 8);
    justify-content: space-between;
    align-items: center;

    .header-left {
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

        &::before {
          display: block;
          content: "";
          width: calc($space * 2);
          height: calc($space * 2);
          background-color: color-mix(in oklab, $green-500 80%, transparent);
          border-radius: 50%;
        }
      }
    }

    .header-right {
      display: flex;
      gap: calc($space * 2);

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
