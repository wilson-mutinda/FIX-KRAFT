<script setup lang="ts">
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue'
import BaseToast from './components/ui/BaseToast.vue'
</script>

<template>

  <div class="bg-surface text-text min-h-screen">

    <Navbar />

    <main>
      <router-view />
    </main>

    <Footer />

    <BaseToast />

  </div>

</template>