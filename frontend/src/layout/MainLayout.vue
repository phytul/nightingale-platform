<script setup lang="ts"></script>

<template>
  <div class="header">Header</div>
  <div class="main-container">
    <RouterView />
  </div>
</template>

<style scoped lang="scss">
.header {
  height: calc($space * 16);
  z-index: 50;
  border-bottom: 1px solid $border-color;
}
</style>
