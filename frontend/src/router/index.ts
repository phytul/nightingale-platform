import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home-page',
    },
    {
      path: '/home-page',
      name: 'HomePage',
      component: () => import('@/views/HomePage.vue'),
    },
    {
      path: '/first-home',
      name: 'FirstHome',
      component: () => import('@/views/FirstHome.vue'),
    },
    {
      path: '/work-list',
      name: 'WorkList',
      component: () => import('@/views/WorkList/index.vue'),
    },
  ],
})

export default router
