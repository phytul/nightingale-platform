import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/home",
      component: () => import("@/layout/MainLayout.vue"),
      children: [
        {
          name: "Home",
          path: "/home",
          component: () => import("@/pages/Home/HomePage.vue"),
        },
        {
          name: "Login",
          path: "/login",
          component: () => import("@/pages/Login/LoginPage.vue"),
        },
        {
          name: "Servers",
          path: "/servers",
          component: () => import("@/pages/Servers/ServersPage.vue"),
        },
        {
          name: "Monitoring",
          path: "/monitoring",
          component: () => import("@/pages/Monitoring/MonitoringPage.vue"),
        },
        {
          name: "Tasks",
          path: "/tasks",
          component: () => import("@/pages/Tasks/TasksPage.vue"),
        },
        {
          name: "Logs",
          path: "/logs",
          component: () => import("@/pages/Logs/LogsPage.vue"),
        },
        {
          name: "Alerts",
          path: "/alerts",
          component: () => import("@/pages/Alerts/AlertsPage.vue"),
        },
        {
          name: "Settings",
          path: "/settings",
          component: () => import("@/pages/Settings/SettingsPage.vue"),
        },
      ],
    },
  ],
});

export default router;
