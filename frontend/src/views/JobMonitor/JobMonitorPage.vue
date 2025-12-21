<script setup lang="ts">
import { reactive } from 'vue'
import { getJobStatusOptions, jobStatusLabelMap, jobStatusTagColorMap } from './constants'

// 作业监控项接口
interface JobMonitorItem {
  id: number
  jobName: string
  executeMachine: string
  status: 'running' | 'success' | 'failed' | 'waiting' | 'stopped'
  progress: number
  startTime: string
  endTime: string
  duration: string
  nextRunTime: string
  logCount: number
  showOperations?: boolean
  selected?: boolean
}

// 查询表单
const formInline = reactive({
  jobName: '',
  executeMachine: '',
  status: '',
  dateRange: '',
})

const onSubmit = () => {
  console.log(formInline)
}

// 作业状态枚举
const jobStatusOptions = getJobStatusOptions()

// 作业监控列表数据
const jobMonitorList = reactive<JobMonitorItem[]>([
  {
    id: 1,
    jobName: '数据备份作业',
    executeMachine: '服务器-01',
    status: 'running',
    progress: 75,
    startTime: new Date().toLocaleString(), // 今日开始
    endTime: '',
    duration: '00:15:30',
    nextRunTime: '2024-01-16 08:00:00',
    logCount: 156,
  },
  {
    id: 2,
    jobName: '日志清理作业',
    executeMachine: '服务器-02',
    status: 'success',
    progress: 100,
    startTime: new Date().toLocaleString(), // 今日开始
    endTime: new Date().toLocaleString(), // 已完成，有结束时间
    duration: '00:05:12',
    nextRunTime: new Date().toLocaleString(), // 今日下次运行
    logCount: 42,
  },
  {
    id: 3,
    jobName: '数据同步作业',
    executeMachine: '服务器-03',
    status: 'failed',
    progress: 45,
    startTime: new Date().toLocaleString(), // 今日开始且失败
    endTime: new Date().toLocaleString(), // 已失败，有结束时间
    duration: '00:03:25',
    nextRunTime: new Date().toLocaleString(), // 今日下次运行
    logCount: 89,
  },
  {
    id: 4,
    jobName: '报表生成作业',
    executeMachine: '服务器-01',
    status: 'waiting',
    progress: 0,
    startTime: '-',
    endTime: '-',
    duration: '-',
    nextRunTime: new Date().toLocaleString(), // 今日下次运行
    logCount: 0,
  },
  {
    id: 5,
    jobName: '系统监控作业',
    executeMachine: '服务器-02',
    status: 'stopped',
    progress: 60,
    startTime: '2024-01-15 07:00:00', // 非今日
    endTime: '2024-01-15 07:10:45', // 已停止，有结束时间
    duration: '00:10:45',
    nextRunTime: '2024-01-17 08:00:00', // 非今日
    logCount: 203,
  },
])
</script>

<template>
  <div class="job-monitor-container">
    <div class="job-monitor-card">
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="作业名">
          <el-input v-model="formInline.jobName" placeholder="请输入作业名" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="formInline.status" placeholder="选择状态" clearable>
            <el-option
              v-for="item in jobStatusOptions"
              :key="item.code"
              :label="item.label"
              :value="item.code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="选择日期">
          <el-date-picker
            v-model="formInline.dateRange"
            type="daterange"
            range-separator="To"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="job-monitor-card">
      <el-table :data="jobMonitorList" row-key="id">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="jobName" label="作业名" />
        <el-table-column prop="executeMachine" label="执行机器" />
        <el-table-column prop="status" label="状态">
          <template #default="scope: { row: JobMonitorItem }">
            <el-tag :type="jobStatusTagColorMap[scope.row.status]">{{
              jobStatusLabelMap[scope.row.status]
            }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间" />
        <el-table-column prop="endTime" label="结束时间" />
        <el-table-column prop="duration" label="执行时间" />
        <el-table-column fixed="right" label="Operations" min-width="120">
          <template #default>
            <el-button link type="primary" size="small">编辑作业</el-button>
            <el-button link type="primary" size="small">启动作业</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="job-monitor-card">
      <el-button>中止作业</el-button>
      <el-button>修改状态</el-button>
    </div>
  </div>
</template>

<style scoped lang="less">
.job-monitor-container {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .job-monitor-card {
    padding: 24px;
    background-color: #fff;
    box-shadow: 0 0 10px #f2f4f5;
    border-radius: 8px;
  }
}

.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}
</style>
