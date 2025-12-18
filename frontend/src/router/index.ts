import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home',
      name: 'Main',
      component: () => import('@/layout/MainLayout.vue'),
      children: [
        {
          path: '/home',
          name: 'Home',
          component: () => import('@/views/Home/HomePage.vue'),
        },
        {
          path: '/job-monitor',
          name: 'JobMonitor',
          component: () => import('@/views/JobMonitor/JobMonitorPage.vue'),
        },
        {
          path: '/edit-job',
          name: 'EditJob',
          component: () => import('@/views/EditJob/EditJobPage.vue'),
        },
        {
          path: '/multi-components',
          name: 'MultiComponents',
          component: () => import('@/views/MultiComponents/MultiComponentsPage.vue'),
        },
      ],
    },
  ],
})

export default router
