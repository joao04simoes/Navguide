<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="app">
    <aside class="sidebar">
      <router-link to="/route" :class="{ active: route.path === '/route' }">Route</router-link>
      <router-link to="/list" :class="{ active: route.path === '/list' }">List</router-link>
    </aside>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
.active {
  font-weight: bold;
  color: blue;
}
</style>
