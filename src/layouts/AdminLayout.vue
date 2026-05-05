<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/admin/Sidebar.vue'
import Topbar from '@/components/admin/Topbar.vue'

const sidebarOpen = ref(true)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<template>
  <div class="flex h-screen bg-gray-100">

    <!-- SIDEBAR -->
    <Sidebar :open="sidebarOpen" />

    <!-- MAIN -->
    <div class="flex-1 flex flex-col overflow-hidden">

      <!-- TOPBAR -->
      <Topbar @toggle-sidebar="toggleSidebar" />

      <!-- CONTENT -->
      <main class="flex-1 overflow-y-auto p-6">

        <transition name="fade" mode="out-in">
          <router-view />
        </transition>

      </main>

    </div>

  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>