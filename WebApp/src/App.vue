<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="app">


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
