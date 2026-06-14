import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/resolution/:id',
      name: 'resolution-detail',
      component: () => import('../views/ResolutionDetail.vue')
    },
    {
      path: '/meetings',
      name: 'meetings',
      component: () => import('../views/Meetings.vue')
    },
    {
      path: '/meetings/:sourceFile',
      name: 'meeting-detail',
      component: () => import('../views/MeetingDetail.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue')
    }
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

export default router
