import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/quiz/:id',
      name: 'quiz',
      component: () => import('@/views/QuizView.vue'),
    },
    {
      path: '/create',
      name: 'create-quiz',
      component: () => import('@/views/QuizCreatorPage.vue'),
    },
  ],
})

export default router
