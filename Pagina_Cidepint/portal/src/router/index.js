import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import ServicesView from '../views/ServicesView.vue'
import RequestView from '../views/RequestView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import LoginView from '../views/LoginView.vue'
import DetalleServiceView from '../views/DetalleServiceView.vue'
import FiltroServiceView from '../views/FiltroServiceView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/services',
      name: 'services',
      component: ServicesView,
    },
    {
      path: '/service_requests',
      name: 'service_requests',
      component: RequestView,
      meta: { requiresAuth: true },
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: StatisticsView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/servicedetalle/:id',
      name: 'servicedetalle',
      component: DetalleServiceView,
    },
    {
      path: '/filtroservice/:i/:n/:p/:d/:t',
      name: 'filtroservice',
      component: FiltroServiceView,
    },
  ]
})


export default router
