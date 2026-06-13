import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ResolutionDetail from '../views/ResolutionDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/resolution/:id',
      name: 'resolution-detail',
      component: ResolutionDetail
    }
  ]
})

export default router
