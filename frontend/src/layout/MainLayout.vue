<script setup lang="ts">
import useCustomTheme from "@/hooks/useCustomTheme";

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
            size="18px"
            icon="mdi mdi-weather-sunny"
            v-if="customTheme.currentTheme === 'customLightTheme'"
          ></v-icon>
          <v-icon
            size="16px"
            icon="mdi mdi-weather-night"
            v-if="customTheme.currentTheme === 'customDarkTheme'"
          ></v-icon
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
  border-bottom: 1px solid $border-color;

  .header-container {
    display: flex;
    height: calc($space * 16);
    max-width: $container-7xl;
    margin: 0 auto;
    padding-inline: calc($space * 8);
    justify-content: space-between;
    align-items: center;

    .v-btn--size-default {
      min-width: 0;
    }
  }

  .header-left {
    .status-tag {
      display: flex;
      gap: calc($space * 2);
      align-items: center;
      padding-block: calc($space * 1.5);
      padding-inline: calc($space * 3);
      border: 1px solid $border-color;
      border-radius: $radius;
      color: $muted-foreground;
      font-size: $text-xm;
      background-color: $muted-color;

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
}
</style>
