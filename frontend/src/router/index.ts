import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import { useUserStore } from '@/stores/user' // 导入用户存储

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/form',
      name: 'form',
      component: () => import('../views/user/dashboard/DashboardView.vue')
    },
    {
      path: '/form/:vote_obj',
      name: 'form-vote-details',
      component: () => import('../views/user/dashboard/DashboardVoteDetails.vue')
    },
    {
      path: '/vote',
      name: 'vote',
      component: () => import('../views/user/vote/VoteView.vue')
    },
    {
      path: '/vote/:vote_obj',
      name: 'vote-details',
      component: () => import('../views/user/vote/VoteDetails.vue'),
      props: true
    },
    {
      path: '/contactus',
      name: 'contactus',
      component: () => import('../views/ContactUs.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/manager',
      name: 'manager',
      component: () => import('../views/ManagerView.vue'),
      children: [
        {
          path: 'home',
          name: 'manager-home',
          component: () => import('../views/manager/ManagerHome.vue')
        },
        {
          path: 'settings',
          name: 'manager-settings',
          component: () => import('../views/manager/ManagerSettings.vue')
        },
        {
          path: 'settings/:vote_obj',
          name: 'manager-settings-vote-details',
          component: () => import('../views/manager/setting/ManagerSettingsVoteDetails.vue'),
          props: true
        },
        {
          path: 'dashboard',
          name: 'manager-dashboard',
          component: () => import('../views/manager/setting/ManagerSettingsDashboards.vue')
        }
      ]
    }
  ]
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isLoggedIn = !!userStore.token

  if (isLoggedIn && to.name === 'login') {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
