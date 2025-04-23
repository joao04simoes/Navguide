import { createRouter, createWebHistory } from 'vue-router'
import RouteView from '../components/route.vue'
import ListView from '../components/list.vue'

const routes = [
    { path: '/', redirect: '/route' },
    { path: '/route', component: RouteView },
    { path: '/list', component: ListView },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
