<script setup lang="ts">
import { ref } from 'vue'
import { Calendar, CircleCheck, CircleClose, Timer } from '@element-plus/icons-vue'

// 运行作业数据
const runningJobs = ref([
  { name: '明日方方昨日任务', status: 'running', startTime: '09:00:00', runningTime: '1小时25分钟' },
  { name: '券小鸡', status: 'error', startTime: '09:00:00', runningTime: '13秒' },
  { name: '搜索蟑螂邮件', status: 'running', startTime: '08:40:00', runningTime: '55分钟' },
  { name: '每日股票组合查询', status: 'success', startTime: '08:25:00', runningTime: '23分钟' }
])
</script>

<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <el-container>
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

      <!-- 主要内容区域 -->
      <el-main class="main">
        <!-- 数据卡片区域 -->
        <div class="cards-container">
          <div class="card-item">
            <div class="card">
              <div class="card-content">
                <div class="card-header">
                  <div class="card-title">今日作业总数</div>
                  <div class="card-icon">
                    <el-icon><Calendar /></el-icon>
                  </div>
                </div>
                <div class="card-value">23</div>
                <div class="card-stats">
                  <div class="stat-item positive">环比上周 +18%</div>
                  <div class="stat-item negative">环比昨天 -9%</div>
                </div>
              </div>
            </div>
          </div>

          <div class="card-item">
            <div class="card">
              <div class="card-content">
                <div class="card-header">
                  <div class="card-title">已完成作业</div>
                  <div class="card-icon">
                    <el-icon><CircleCheck /></el-icon>
                  </div>
                </div>
                <div class="card-value">18</div>
                <div class="card-stats">
                  <div class="stat-item">今日作业未完成</div>
                  <div class="stat-item">当前完成率 75%</div>
                </div>
              </div>
            </div>
          </div>

          <div class="card-item">
            <div class="card">
              <div class="card-content">
                <div class="card-header">
                  <div class="card-title">作业报错</div>
                  <div class="card-icon">
                    <el-icon><CircleClose /></el-icon>
                  </div>
                </div>
                <div class="card-value">2</div>
                <div class="card-stats">
                  <div class="stat-item">今日共处理错误数 2</div>
                  <div class="stat-item negative">今日新增错误数 -1</div>
                </div>
              </div>
            </div>
          </div>

          <div class="card-item">
            <div class="card">
              <div class="card-content">
                <div class="card-header">
                  <div class="card-title">正在运行</div>
                  <div class="card-icon">
                    <el-icon><Timer /></el-icon>
                  </div>
                </div>
                <div class="card-value">3</div>
                <div class="card-stats">
                  <div class="stat-item">今日作业平均运行时间 24分钟</div>
                  <div class="stat-item positive">运行速度提升 +18%</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 当前运行作业详情 -->
        <div class="running-jobs-section">
          <div class="running-jobs-card">
            <div class="job-list">
              <div v-for="(job, index) in runningJobs" :key="index" class="job-item">
                <div class="job-info">
                  <div class="job-status" :class="'status-' + job.status"></div>
                  <div class="job-name">{{ job.name }}</div>
                </div>
                <div class="job-time-info">
                  <div class="job-time">
                    <span class="time-label">启动时间:</span>
                    <span class="time-value">{{ job.startTime }}</span>
                  </div>
                  <div class="job-time">
                    <span class="time-label">已运行时间:</span>
                    <span class="time-value">{{ job.runningTime }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分页指示器 -->
            <div class="pagination-indicator">
              <div v-for="i in 5" :key="i" class="page-dot" :class="{ active: i === 1 }"></div>
            </div>
          </div>
        </div>
      </el-main>

      <!-- 底部标志区域 -->
      <el-footer class="footer">
        <div class="footer-content">
          <el-avatar :size="40" src="https://via.placeholder.com/40"></el-avatar>
          <div class="logo-text">Nightingale</div>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<style scoped>
.dashboard {
  width: 100%;
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  padding: 16px;
}

/* 顶部导航栏 */
.header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 16px 24px;
  background-color: #ffffff;
  border-radius: 8px;
  margin-bottom: 16px;
  height: auto;
}

.header-left {
  margin-right: 32px;
}

.nav {
  border-bottom: none;
}

/* 高亮菜单项样式 */
.nav .el-menu-item.is-active {
  background-color: #1890ff;
  color: #ffffff;
  border-radius: 4px;
  padding: 0 16px;
}

/* 主要内容区域 */
.main {
  background-color: #f5f7fa;
  padding: 0;
}

/* 数据卡片区域 */
/* 卡片容器 */
.cards-container {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin: 24px 16px;
  padding: 0 8px;
}

/* 卡片项 */
.card-item {
  min-width: 290px;
  flex: 1;
}

/* 卡片样式 */
.card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  padding: 16px;
  height: 100%;
  min-height: 210px;
  display: flex;
  flex-direction: column;
}
.card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.card-title {
  font-size: 14px;
  color: #5f6368;
  margin: 0;
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #1890ff;
}

.card-value {
  font-size: 32px;
  font-weight: 600;
  color: #202124;
  margin-bottom: 12px;
}

.card-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-item {
  font-size: 12px;
  color: #5f6368;
  line-height: 1.4;
}

.stat-item.positive {
  color: #52c41a;
}

.stat-item.negative {
  color: #f5222d;
}

/* 当前运行作业详情 */
.running-jobs-section {
  margin-top: 16px;
}

.running-jobs-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 16px;
}

/* 作业列表样式 */
.job-list {
  margin-top: 8px;
}

.job-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.job-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.job-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.status-running {
  background-color: #fadb14;
}

.status-error {
  background-color: #f5222d;
}

.status-success {
  background-color: #52c41a;
}

.job-name {
  font-size: 14px;
  color: #202124;
  font-weight: 400;
}

.job-time-info {
  display: flex;
  gap: 32px;
}

.job-time {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  font-size: 12px;
}

.time-label {
  color: #5f6368;
}

.time-value {
  color: #202124;
  font-weight: 400;
}

/* 分页指示器 */
.pagination-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 20px;
}

.page-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #d9d9d9;
}

.page-dot.active {
  background-color: #1890ff;
}

/* 底部标志区域 */
.footer {
  padding: 20px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.footer-content {
  background-color: transparent;
  border: none;
  border-radius: 8px;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: none;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #202124;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 16px;
  }
  
  .nav {
    width: 100%;
  }
  
  .job-time-info {
    flex-direction: column;
    gap: 8px;
    align-items: flex-end;
  }
}
</style>