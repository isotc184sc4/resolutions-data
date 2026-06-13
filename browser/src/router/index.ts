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
      path: '/meetings/:meetingId/resolution/:resolutionId',
      name: 'resolution-by-meeting',
      component: ResolutionDetail
    },
    {
      path: '/resolution/:id',
      name: 'resolution-detail',
      component: ResolutionDetail
    }
  ]
})

export default router
