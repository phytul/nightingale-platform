<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Document, Menu as IconMenu, Location, Setting } from '@element-plus/icons-vue'

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<template>
  <div class="sider-menus">
    <el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
    >
      <el-menu-item index="1">
        <el-icon><setting /></el-icon>
        <span>参数设置</span>
      </el-menu-item>

      <el-sub-menu index="2">
        <template #title>
          <el-icon><location /></el-icon>
          <span>作业分层</span>
        </template>
        <el-menu-item index="1-1">基础作业层</el-menu-item>
        <el-menu-item index="1-2">中间作业层</el-menu-item>
        <el-menu-item index="1-3">结果作业层</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<style scoped lang="less"></style>
