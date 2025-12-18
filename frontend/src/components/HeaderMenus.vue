<script setup lang="ts">
import { reactive } from 'vue'

const menus = reactive([
  {
    name: '首页',
    route: '/home',
  },
  {
    name: '运行监控',
    route: '/job-monitor',
  },
  {
    name: '编辑作业',
    route: '/edit-job',
  },
  {
    name: '组件',
    route: '/multi-components',
  },
])
</script>

<template>
  <el-header height="auto" class="header">
    <div class="avatar-box">
      <el-avatar :size="60" src="https://via.placeholder.com/40">头像</el-avatar>
    </div>
    <el-menu router :default-active="$route.path" mode="horizontal" background-color="transparent">
      <el-menu-item v-for="item in menus" :key="item.route" :index="item.route">{{
        item.name
      }}</el-menu-item>
    </el-menu>
  </el-header>
</template>

<style scoped lang="less">
.header {
  position: sticky;
  height: 80px;
  top: 0;
  display: flex;
  box-sizing: border-box;
  justify-content: flex-start;
  align-items: center;
  padding: 0 24px;
  background-color: #ffffff;
  z-index: 99;
  box-shadow: 0 0 10px #dbdbdb;
}

.avatar-box {
  display: flex;
  align-items: center;
  margin-right: 64px;
}

.el-menu {
  display: flex;
  align-items: flex-end;
  box-sizing: border-box;
  padding-top: 16px;
  gap: 8px;
  flex: 1;
  border-bottom: none;
  height: 100%;

  .el-menu-item {
    height: 60px;
    border-radius: 20px 20px 0 0;
    padding: 0 16px;
    cursor: pointer;
    border: none;
    font-size: 18px;
    color: #333;
    user-select: none;

    &.is-active {
      background-color: #4675e2;
      color: #fff !important;
      font-weight: 600;
    }

    &:not(.is-active):hover {
      background-color: #f2f4f5;
      color: #666;
    }
  }
}
</style>
