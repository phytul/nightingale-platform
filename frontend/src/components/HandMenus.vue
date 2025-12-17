<script setup lang="ts"></script>

<template>
    <el-header height="auto" class="header">
        <div class="header-left">
          <el-avatar :size="40" src="https://via.placeholder.com/40">头像位置</el-avatar>
        </div>
        <el-menu
          :default-active="'3'"
          mode="horizontal"
          background-color="transparent"
          text-color="#202124"
          active-text-color="#ffffff"
          class="nav"
        >
          <el-menu-item index="1">作业列表  </el-menu-item>
          <el-menu-item index="2">运行监控  </el-menu-item>
          <el-menu-item index="3">编辑作业  </el-menu-item>
          <el-menu-item index="4">组件 </el-menu-item>
        </el-menu>
      </el-header>
</template>

<style scoped></style>
