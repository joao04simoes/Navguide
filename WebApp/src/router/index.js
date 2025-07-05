import { createRouter, createWebHistory } from 'vue-router'
import RouteView from '../components/route.vue'
import ListView from '../components/list.vue'
import home from '../components/home.vue'
import funcionario from '../components/funcionario.vue'
import modoNormal from '../components/modo-normal.vue'
import buss from '../components/buss.vue'

const routes = [
    { path: '/', component: home },
    { path: '/route', component: RouteView },
    { path: '/list', component: ListView },
    { path: '/home', component: home },
    { path: '/funcionario', component: funcionario },
    { path: '/modo-normal', component: modoNormal },
    { path: '/buss', component: buss },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
