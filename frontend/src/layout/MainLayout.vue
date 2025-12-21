<script setup lang="ts">
import HeaderMenus from '@/components/HeaderMenus.vue'
</script>

<template>
  <HeaderMenus />
  <div class="main-container">
    <RouterView />
  </div>
</template>

<style scoped>
.main-container {
  background-color: #f5f7fa;
  min-height: 100vh;
}
</style>
