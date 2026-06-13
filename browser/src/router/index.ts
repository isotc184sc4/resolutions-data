import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ResolutionDetail from '../views/ResolutionDetail.vue'
import Meetings from '../views/Meetings.vue'
import MeetingDetail from '../views/MeetingDetail.vue'

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
    },
    {
      path: '/meetings',
      name: 'meetings',
      component: Meetings
    },
    {
      path: '/meetings/:sourceFile',
      name: 'meeting-detail',
      component: MeetingDetail
    }
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
