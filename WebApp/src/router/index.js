import { createRouter, createWebHistory } from 'vue-router'
import RouteView from '../components/route.vue'
import ListView from '../components/list.vue'
import home from '../components/home.vue'
import criar_lista from '../components/criar-lista.vue'

const routes = [
    { path: '/', component: home },
    { path: '/route', component: RouteView },
    { path: '/list', component: ListView },
    { path: '/home', component: home },
    { path: '/criar-lista', component: criar_lista },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
