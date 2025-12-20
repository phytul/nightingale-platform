/**
 * 任务状态名称 Map
 */
export const jobStatusLabelMap = {
  running: '运行中',
  success: '成功',
  failed: '失败',
  waiting: '等待中',
  stopped: '中止',
}

/**
 * 任务状态标签 Map
 */
export const jobStatusTagColorMap = {
  running: 'primary',
  success: 'success',
  failed: 'danger',
  waiting: 'warning',
  stopped: 'info',
}

/**
 * 获取 JobStatusLabelMap 的 key 类型
 */
export type JobStatusLabelMapKey = keyof typeof jobStatusLabelMap
