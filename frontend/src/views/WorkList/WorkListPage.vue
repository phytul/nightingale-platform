<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Edit, Delete, View } from '@element-plus/icons-vue'

// 工作项接口
interface WorkItem {
  id: number
  title: string
  description: string
  status: 'pending' | 'in-progress' | 'completed'
  priority: 'low' | 'medium' | 'high'
  assignee: string
  dueDate: string
  createdAt: string
}

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')

// 工作列表数据
const workList = ref<WorkItem[]>([
  {
    id: 1,
    title: '前端页面开发',
    description: '完成用户管理模块的前端页面开发',
    status: 'in-progress',
    priority: 'high',
    assignee: '张三',
    dueDate: '2024-01-15',
    createdAt: '2024-01-01',
  },
  {
    id: 2,
    title: 'API接口测试',
    description: '测试用户登录和注册API接口',
    status: 'pending',
    priority: 'medium',
    assignee: '李四',
    dueDate: '2024-01-20',
    createdAt: '2024-01-02',
  },
  {
    id: 3,
    title: '数据库优化',
    description: '优化用户表查询性能',
    status: 'completed',
    priority: 'low',
    assignee: '王五',
    dueDate: '2024-01-10',
    createdAt: '2024-01-03',
  },
])

// 对话框状态
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()

// 表单数据
const form = reactive({
  id: 0,
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
  assignee: '',
  dueDate: '',
})

// 表单规则
const rules = {
  title: [{ required: true, message: '请输入工作标题', trigger: 'blur' }],
  description: [{ required: true, message: '请输入工作描述', trigger: 'blur' }],
  assignee: [{ required: true, message: '请输入负责人', trigger: 'blur' }],
  dueDate: [{ required: true, message: '请选择截止日期', trigger: 'change' }],
}

// 筛选后的工作列表
const filteredWorkList = computed(() => {
  return workList.value.filter((item) => {
    const matchSearch =
      item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchStatus = !statusFilter.value || item.status === statusFilter.value
    const matchPriority = !priorityFilter.value || item.priority === priorityFilter.value

    return matchSearch && matchStatus && matchPriority
  })
})

// 状态标签样式
const getStatusType = (status: string) => {
  const statusMap = {
    pending: 'info',
    'in-progress': 'warning',
    completed: 'success',
  }
  return statusMap[status as keyof typeof statusMap] || 'info'
}

const getStatusLabel = (status: string) => {
  const statusMap = {
    pending: '待处理',
    'in-progress': '进行中',
    completed: '已完成',
  }
  return statusMap[status as keyof typeof statusMap] || status
}

// 优先级标签样式
const getPriorityType = (priority: string) => {
  const priorityMap = {
    low: 'success',
    medium: 'warning',
    high: 'danger',
  }
  return priorityMap[priority as keyof typeof priorityMap] || 'info'
}

const getPriorityLabel = (priority: string) => {
  const priorityMap = {
    low: '低',
    medium: '中',
    high: '高',
  }
  return priorityMap[priority as keyof typeof priorityMap] || priority
}

// 添加工作
const handleAdd = () => {
  dialogTitle.value = '添加工作'
  dialogVisible.value = true
  Object.assign(form, {
    id: 0,
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    assignee: '',
    dueDate: '',
  })
}

// 编辑工作
const handleEdit = (row: WorkItem) => {
  dialogTitle.value = '编辑工作'
  dialogVisible.value = true
  Object.assign(form, {
    id: row.id,
    title: row.title,
    description: row.description,
    status: row.status,
    priority: row.priority,
    assignee: row.assignee,
    dueDate: row.dueDate,
  })
}

// 删除工作
const handleDelete = async (row: WorkItem) => {
  try {
    await ElMessageBox.confirm('确定要删除这项工作吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    const index = workList.value.findIndex((item) => item.id === row.id)
    if (index !== -1) {
      workList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  } catch (error) {
    // 用户取消删除
    console.error('删除工作失败:', error)
  }
}

// 查看详情
const handleView = (row: WorkItem) => {
  ElMessage.info(`查看工作：${row.title}`)
}

// 提交表单
const submitForm = async () => {
  try {
    await formRef.value.validate()

    if (form.id) {
      // 编辑
      const index = workList.value.findIndex((item) => item.id === form.id)
      if (index !== -1) {
        workList.value[index] = {
          ...workList.value[index],
          ...form,
        } as WorkItem
        ElMessage.success('编辑成功')
      }
    } else {
      // 添加
      const newWork: WorkItem = {
        ...form,
        id: Date.now(),
        createdAt: new Date().toISOString().split('T')[0] || '',
      } as WorkItem
      workList.value.push(newWork)
      ElMessage.success('添加成功')
    }

    dialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 重置表单
const resetForm = () => {
  formRef.value?.resetFields()
}
</script>

<template>
  <div class="work-list-container">
    <div class="header">
      <h2>工作列表</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd">添加工作</el-button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索工作标题或描述"
            :prefix-icon="Search"
            clearable
          />
        </el-col>
        <el-col :span="6">
          <el-select v-model="statusFilter" placeholder="筛选状态" clearable>
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in-progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="priorityFilter" placeholder="筛选优先级" clearable>
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <!-- 工作列表表格 -->
    <div class="table-container">
      <el-table :data="filteredWorkList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="工作标题" min-width="200" />
        <el-table-column prop="description" label="工作描述" min-width="300" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)">
              {{ getPriorityLabel(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="assignee" label="负责人" width="120" />
        <el-table-column prop="dueDate" label="截止日期" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" :icon="View" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="warning" size="small" :icon="Edit" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" :icon="Delete" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="工作标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入工作标题" />
        </el-form-item>
        <el-form-item label="工作描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入工作描述"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态">
                <el-option label="待处理" value="pending" />
                <el-option label="进行中" value="in-progress" />
                <el-option label="已完成" value="completed" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="form.priority" placeholder="请选择优先级">
                <el-option label="低" value="low" />
                <el-option label="中" value="medium" />
                <el-option label="高" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="负责人" prop="assignee">
              <el-input v-model="form.assignee" placeholder="请输入负责人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="截止日期" prop="dueDate">
              <el-date-picker
                v-model="form.dueDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="less">
.work-list-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header {
  h2 {
    margin: 0;
    color: #303133;
  }
}

.filter-container {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-table) {
  border-radius: 4px;
}

:deep(.el-tag) {
  border-radius: 4px;
}
</style>
