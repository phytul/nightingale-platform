<script setup lang="ts">
export type Props = {
  noPadding?: boolean
}
const props = defineProps<Props>()
const { noPadding } = props
</script>

<template>
  <div
    class="page-contain"
    :style="{
      padding: noPadding ? 0 : undefined,
    }"
  >
    <slot></slot>
  </div>
</template>

<style scoped lang="less">
.page-contain {
  height: 100%;
  padding: 16px;
}
</style>
