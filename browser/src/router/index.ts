import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ResolutionDetail from '../views/ResolutionDetail.vue'

const router = createRouter({
  history: createWebHashHistory(),
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
