<script setup lang="ts">
import PageContain from '@/components/PageContain.vue'
import SiderMenus from './components/SiderMenus.vue'
import CustomTabs from './components/CustomTabs.vue'
</script>

<template>
  <PageContain no-padding>
    <div class="edit-job-page-contain">
      <div class="edit-job-sider">
        <SiderMenus />
      </div>
      <div class="edit-job-tabs">
        <CustomTabs />
      </div>
    </div>
  </PageContain>
</template>

<style scoped lang="less">
.edit-job-page-contain {
  display: flex;
  height: 100%;

  .edit-job-sider {
    width: 200px;
    height: 100%;
    background-color: #fff;
  }

  .edit-job-tabs {
    flex: 1;
  }
}
</style>
