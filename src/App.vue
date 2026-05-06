<script setup lang="ts">
import Footer from './components/Footer.vue';
import Navbar from './components/Navbar.vue';

</script>

<template>
  <div class="bg-surface text-text min-h-screen">
    <Navbar />
    <main>
      <router-view></router-view>
    </main>

    <Footer />
  </div>
</template>