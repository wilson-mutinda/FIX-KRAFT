<script setup lang="ts">
import { useRoute } from 'vue-router';
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue'
import BaseToast from './components/ui/BaseToast.vue'
import { computed } from 'vue';

const route = useRoute()
const isAdminRoute = computed(() => route.path.startsWith('/admin'))

</script>

<template>

  <div class="bg-surface text-text min-h-screen">

    <Navbar v-if="!isAdminRoute" />

    <main>
      <router-view />
    </main>

    <Footer v-if="!isAdminRoute" />

    <BaseToast />

  </div>

</template>