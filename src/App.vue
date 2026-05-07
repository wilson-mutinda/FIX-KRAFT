<script setup lang="ts">
import Footer from './components/Footer.vue';
import Navbar from './components/Navbar.vue';
import Toast from './components/ui/Toast.vue';
import { useNotifications } from './stores/notifications';

const notifications = useNotifications()

</script>

<template>
  <div class="bg-surface text-text min-h-screen">
    <Navbar />
    <main>
      <router-view></router-view>

      <div class="fixed top-5 right-5 z-50 space-y-3">

        <Toast 
        v-for="n in notifications.notifications" 
        :key="n.id" 
        :message="n.message" 
        :type="n.type" />
      </div>
    </main>

    <Footer />
  </div>
</template>