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
      ],
    },
  ],
});

export default router;
