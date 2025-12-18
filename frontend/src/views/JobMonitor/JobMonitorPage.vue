<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, ArrowDown } from '@element-plus/icons-vue'

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

// 查询条件
const searchForm = reactive({
  jobName: '',
  executeMachine: '',
  status: '',
  todayErrors: false,
  todayJobs: false,
  startDate: '',
  endDate: ''
})

// 批量操作
const batchOperation = reactive({
  hasSelected: false,
  selectedCount: 0
})

// 编辑弹窗
const editDialogVisible = ref(false)
const currentEditRow = ref<JobMonitorItem | null>(null)
const editForm = reactive({
  jobName: '',
  executeMachine: '',
  status: ''
})

// 作业监控列表数据
const jobMonitorList = ref<JobMonitorItem[]>([
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
    logCount: 156
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
    logCount: 42
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
    logCount: 89
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
    logCount: 0
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
    logCount: 203
  }
])

// 自动刷新定时器
let refreshTimer: number | null = null

// 判断日期是否为今天
const isToday = (dateStr: string) => {
  if (!dateStr || dateStr === '-') return false
  
  const today = new Date()
  const date = new Date(dateStr)
  
  return today.getFullYear() === date.getFullYear() &&
    today.getMonth() === date.getMonth() &&
    today.getDate() === date.getDate()
}

// 筛选后的作业监控列表
const filteredJobMonitorList = computed(() => {
  return jobMonitorList.value.filter(item => {
    const matchJobName = !searchForm.jobName || item.jobName.includes(searchForm.jobName)
    const matchMachine = !searchForm.executeMachine || item.executeMachine === searchForm.executeMachine
    const matchStatus = !searchForm.status || item.status === searchForm.status
    
    // 今日报错：只显示今日报错的作业
    const matchTodayErrors = !searchForm.todayErrors || 
      (item.status === 'failed' && isToday(item.startTime))
    
    // 今日作业：只显示今日会执行的作业
    const matchTodayJobs = !searchForm.todayJobs || 
      (isToday(item.startTime) || isToday(item.nextRunTime))
    
    // 日期范围过滤
    let matchDateRange = true
    if (searchForm.startDate || searchForm.endDate) {
      let itemDate = new Date(item.startTime)
      if (item.startTime === '-') {
        // 如果开始时间为空，则使用下次运行时间
        if (item.nextRunTime !== '-') {
          itemDate = new Date(item.nextRunTime)
        } else {
          matchDateRange = false
        }
      }
      
      if (matchDateRange && itemDate) {
        if (searchForm.startDate && itemDate < new Date(searchForm.startDate)) {
          matchDateRange = false
        }
        if (searchForm.endDate) {
          const endDate = new Date(searchForm.endDate)
          endDate.setHours(23, 59, 59, 999) // 设置为当天的结束时间
          if (itemDate > endDate) {
            matchDateRange = false
          }
        }
      }
    }
    
    return matchJobName && matchMachine && matchStatus && matchTodayErrors && matchTodayJobs && matchDateRange
  })
})

// 获取所有执行机器选项
const machineOptions = computed(() => {
  const machines = [...new Set(jobMonitorList.value.map(item => item.executeMachine))]
  return machines.map(machine => ({ value: machine, label: machine }))
})

// 获取状态选项
const statusOptions = [
  { value: 'running', label: '运行中' },
  { value: 'success', label: '成功' },
  { value: 'failed', label: '失败' },
  { value: 'waiting', label: '等待中' },
  { value: 'stopped', label: '已停止' }
]

// 获取状态小圆点颜色
const getStatusDotColor = (status: string) => {
  // 蓝色-已经部署的作业/正在等待任务
  // 红色-未部署作业/执行错误任务
  // 黄色-正在执行任务
  // 绿色-执行成功任务
  const colorMap = {
    'running': '#E6A23C',  // 黄色-正在执行任务
    'success': '#67C23A',  // 绿色-执行成功任务
    'failed': '#F56C6C',   // 红色-执行错误任务
    'waiting': '#409EFF',  // 蓝色-正在等待任务
    'stopped': '#909399'   // 灰色-已停止任务
  }
  return colorMap[status as keyof typeof colorMap] || '#909399'
}

// 获取行类名，用于选中行高亮
const getRowClassName = ({ row }: { row: JobMonitorItem }) => {
  return row.selected ? 'selected-row' : ''
}

// 查询作业
const handleSearch = () => {
  ElMessage.success('查询完成')
}

// 今日报错
const handleTodayErrors = () => {
  searchForm.jobName = ''
  searchForm.executeMachine = ''
  searchForm.status = 'failed'
  searchForm.todayErrors = true
  searchForm.todayJobs = false
  searchForm.startDate = ''
  searchForm.endDate = ''
  ElMessage.success('已筛选今日报错作业')
}

// 今日作业
const handleTodayJobs = () => {
  searchForm.jobName = ''
  searchForm.executeMachine = ''
  searchForm.status = ''
  searchForm.todayErrors = false
  searchForm.todayJobs = true
  searchForm.startDate = ''
  searchForm.endDate = ''
  ElMessage.success('已筛选今日执行作业')
}

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  const parts = command.split('-')
  if (parts.length < 2) {
    ElMessage.error('命令格式错误')
    return
  }
  
  const [action, idStr] = parts
  if (!idStr) {
    ElMessage.error('命令格式错误：缺少作业ID')
    return
  }
  
  const id = parseInt(idStr)
  const job = jobMonitorList.value.find(item => item.id === id)
  
  if (!job) {
    ElMessage.error('未找到对应的作业')
    return
  }
  
  switch (action) {
    case 'edit':
      // 编辑作业
      currentEditRow.value = job
      editForm.jobName = job.jobName
      editForm.executeMachine = job.executeMachine
      editForm.status = job.status
      editDialogVisible.value = true
      break
    case 'runOnce':
      // 启动一次
      ElMessage.success(`已启动作业: ${job.jobName}`)
      job.status = 'running'
      job.progress = 0
      job.startTime = new Date().toLocaleString()
      job.endTime = '-'
      break
    case 'addTiming':
      // 添加定时
      ElMessage.success(`已为作业 ${job.jobName} 添加定时`)
      break
    case 'editTiming':
      // 编辑定时
      ElMessage.success(`正在编辑作业 ${job.jobName} 的定时设置`)
      break
  }
}

// 编辑作业
const handleEditJob = () => {
  if (!currentEditRow.value) {
    ElMessage.error('未选择要编辑的作业')
    return
  }
  
  // 更新作业信息
  const index = jobMonitorList.value.findIndex(item => item.id === currentEditRow.value!.id)
  if (index !== -1) {
    const item = jobMonitorList.value[index]
    if (item) {
      item.jobName = editForm.jobName
      item.executeMachine = editForm.executeMachine
      item.status = editForm.status as 'running' | 'success' | 'failed' | 'waiting' | 'stopped'
    }
  }
  
  ElMessage.success('作业信息已更新')
  editDialogVisible.value = false
}

// 关闭编辑弹窗
const handleCloseEditDialog = () => {
  editDialogVisible.value = false
}

// 处理选中状态变化
const handleSelectionChange = (selection: JobMonitorItem[]) => {
  batchOperation.selectedCount = selection.length
  batchOperation.hasSelected = selection.length > 0
  
  // 更新列表中的选中状态
  jobMonitorList.value.forEach(item => {
    item.selected = selection.some(selected => selected.id === item.id)
  })
}

// 批量结束执行并修改状态为正常
const handleBatchStopAndSetNormal = () => {
  const selectedJobs = jobMonitorList.value.filter(item => item.selected)
  
  if (selectedJobs.length === 0) {
    ElMessage.warning('请先选择要操作的作业')
    return
  }
  
  let updatedCount = 0
  selectedJobs.forEach(job => {
    // 只对正在运行的作业进行操作
    if (job.status === 'running') {
      job.status = 'success' // 修改为正常状态
      job.endTime = new Date().toLocaleString() // 设置结束时间
      job.progress = 100 // 设置进度为100%
      updatedCount++
    }
  })
  
  ElMessage.success(`已成功结束 ${updatedCount} 个作业并设置为正常状态`)
  
  // 清除所有选中状态
  jobMonitorList.value.forEach(item => {
    item.selected = false
  })
  batchOperation.selectedCount = 0
  batchOperation.hasSelected = false
}

// 执行结束（kill正在运行的作业）
const handleKillRunningJobs = () => {
  const selectedJobs = jobMonitorList.value.filter(item => item.selected)
  
  if (selectedJobs.length === 0) {
    ElMessage.warning('请先选择要操作的作业')
    return
  }
  
  let killedCount = 0
  selectedJobs.forEach(job => {
    // 只对正在运行的作业进行kill操作
    if (job.status === 'running') {
      job.status = 'stopped' // 修改为停止状态
      job.endTime = new Date().toLocaleString() // 设置结束时间
      killedCount++
    }
  })
  
  ElMessage.success(`已成功kill ${killedCount} 个正在运行的作业`)
  
  // 清除所有选中状态
  jobMonitorList.value.forEach(item => {
    item.selected = false
  })
  batchOperation.selectedCount = 0
  batchOperation.hasSelected = false
}

// 作业状态变为正常（报错的作业变为已完成状态）
const handleSetFailedJobsToCompleted = () => {
  const selectedJobs = jobMonitorList.value.filter(item => item.selected)
  
  if (selectedJobs.length === 0) {
    ElMessage.warning('请先选择要操作的作业')
    return
  }
  
  let updatedCount = 0
  selectedJobs.forEach(job => {
    // 对报错的作业进行操作
    if (job.status === 'failed') {
      job.status = 'success' // 修改为已完成状态
      if (job.endTime === '-') {
        job.endTime = new Date().toLocaleString() // 如果没有结束时间，设置当前时间
      }
      updatedCount++
    }
  })
  
  ElMessage.success(`已成功将 ${updatedCount} 个报错作业的状态设置为已完成`)
  
  // 清除所有选中状态
  jobMonitorList.value.forEach(item => {
    item.selected = false
  })
  batchOperation.selectedCount = 0
  batchOperation.hasSelected = false
}

// 开启自动刷新
const startAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    // 模拟数据更新
    jobMonitorList.value.forEach(item => {
      if (item.status === 'running' && item.progress < 100) {
        item.progress = Math.min(item.progress + Math.floor(Math.random() * 5) + 1, 100)
        if (item.progress === 100) {
          item.status = 'success'
        }
      }
    })
  }, 3000)
}

// 组件挂载时开启自动刷新
onMounted(() => {
  startAutoRefresh()
})

// 组件卸载时清除定时器
onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
})
</script>

<template>
  <div class="job-monitor-container">
    <!-- 查询条件 -->
    <div class="search-container">
      <el-form :model="searchForm" inline>
        <el-form-item label="作业名">
          <el-input
            v-model="searchForm.jobName"
            placeholder="请输入作业名"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="执行机器">
          <el-select
            v-model="searchForm.executeMachine"
            placeholder="请选择执行机器"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="item in machineOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 150px"
          >
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="起始日期">
          <el-date-picker
            v-model="searchForm.startDate"
            type="date"
            placeholder="请选择起始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker
            v-model="searchForm.endDate"
            type="date"
            placeholder="请选择结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
          <el-button type="danger" @click="handleTodayErrors">今日报错</el-button>
          <el-button type="warning" @click="handleTodayJobs">今日作业</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 作业监控列表 -->
    <div class="table-container">
      <!-- 批量操作栏 -->
      <div class="batch-operation-bar" v-if="batchOperation.hasSelected">
        <span>已选择 {{ batchOperation.selectedCount }} 项</span>
        <el-button 
          type="danger" 
          size="small" 
          @click="handleBatchStopAndSetNormal"
          style="margin-left: 10px;"
        >
          结束执行并设为正常
        </el-button>
      </div>
      
      <el-table 
        :data="filteredJobMonitorList" 
        style="width: 100%" 
        border
        @selection-change="handleSelectionChange"
        :row-class-name="getRowClassName"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column label="作业名" min-width="150">
          <template #default="{ row }">
            <div style="display: flex; align-items: center;">
              <span 
                class="status-dot" 
                :style="{ backgroundColor: getStatusDotColor(row.status) }"
              ></span>
              {{ row.jobName }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="executeMachine" label="执行机器" width="150" />
        <el-table-column prop="startTime" label="开始时间" width="180" />
        <el-table-column prop="duration" label="运行时长" width="120" />
        <el-table-column prop="endTime" label="结束时间" width="180" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-dropdown trigger="click" @command="handleCommand">
              <el-button
                type="primary"
                size="small"
              >
                编辑<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="`edit-${row.id}`">编辑作业</el-dropdown-item>
                  <el-dropdown-item :command="`runOnce-${row.id}`">启动一次</el-dropdown-item>
                  <el-dropdown-item :command="`addTiming-${row.id}`">添加定时</el-dropdown-item>
                  <el-dropdown-item :command="`editTiming-${row.id}`">编辑定时</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 底部操作按钮 -->
      <div class="bottom-operation-bar">
        <span v-if="batchOperation.hasSelected">已选择 {{ batchOperation.selectedCount }} 项</span>
        <span v-else>请选择要操作的作业</span>
        <div class="operation-buttons">
          <el-button 
            type="danger" 
            @click="handleKillRunningJobs"
            :disabled="!batchOperation.hasSelected"
          >
            执行结束（kill）
          </el-button>
          <el-button 
            type="success" 
            @click="handleSetFailedJobsToCompleted"
            :disabled="!batchOperation.hasSelected"
          >
            作业状态变为正常
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 编辑作业弹窗 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑作业"
      width="500px"
      :before-close="handleCloseEditDialog"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="作业名称">
          <el-input v-model="editForm.jobName" placeholder="请输入作业名称"></el-input>
        </el-form-item>
        <el-form-item label="执行机器">
          <el-select v-model="editForm.executeMachine" placeholder="请选择执行机器" style="width: 100%">
            <el-option
              v-for="item in machineOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="作业状态">
          <el-select v-model="editForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCloseEditDialog">取消</el-button>
          <el-button type="primary" @click="handleEditJob">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.job-monitor-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #303133;
}

.search-container {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.table-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.batch-operation-bar {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.bottom-operation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.operation-buttons {
  display: flex;
  gap: 10px;
}

.selected-row {
  background-color: #f0f9ff !important;
}

:deep(.el-table) {
  border-radius: 4px;
}

:deep(.el-tag) {
  border-radius: 4px;
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}

:deep(.el-progress-bar__inner) {
  border-radius: 4px;
}

.status-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
}
</style>