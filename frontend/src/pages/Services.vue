<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import { useServicesStore } from '@/stores/services'
import { onMounted } from 'vue'

const store = useServicesStore()

onMounted(() => {
  store.load()
})
</script>

<template>
  <div class="bg-white dark:bg-gray-900">

    <!-- HERO -->
    <section class="py-24 bg-gradient-to-br from-secondary to-black text-white text-center">
      <div class="max-w-4xl mx-auto px-6" data-aos="fade-up">

        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          Services That Build
          <span class="text-primary">Real Products</span>
        </h1>

        <p class="text-gray-300 text-lg mb-6">
          We don&apos;t just design — we engineer scalable digital systems for modern businesses.
        </p>

        <!-- <button
          @click="$router.push('/contact')"
          class="bg-primary px-6 py-3 rounded-xl shadow-lg hover:scale-105 transition"
        >
          Start Your Project
        </button> -->

        <base-button @click="$router.push('/contact')">
        Start Your Project
      </base-button>

      </div>
    </section>

    <!-- SERVICES -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800 rounded-2xl">
      <div class="max-w-7xl mx-auto px-6">

        <h2 class="text-3xl font-bold text-center mb-12 text-gray-600 dark:text-gray-300" data-aos="fade-up">
          What We Offer
        </h2>

        <!-- FADE TRANSITION WRAPPER -->
        <transition-group
          name="fade"
          tag="div"
          class="grid md:grid-cols-3 gap-8"
        >

          <div
            v-for="service in store.services"
            :key="service.id"
            data-aos="zoom-in"
            class="p-6 bg-gray-50 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-2 transition"
          >

            <!-- IMAGE -->
            <img
              :src="service.image"
              class="rounded-lg mb-4 h-40 w-full object-cover"
            />

            <!-- TITLE -->
            <h3 class="text-xl font-semibold mb-2">
              {{ service.title }}
            </h3>

            <!-- DESCRIPTION -->
            <p class="text-gray-600 text-sm mb-4">
              {{ service.description }}
            </p>

            <!-- FEATURES -->
            <ul class="text-sm text-gray-500 space-y-1">
              <li v-for="(f, i) in service.features" :key="i">
                • {{ f }}
              </li>
            </ul>

          </div>

        </transition-group>

      </div>
    </section>

    <!-- PROCESS -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800 rounded-2xl">
      <div class="max-w-5xl mx-auto px-6 text-center">

        <h2 class="text-3xl font-bold mb-10 text-gray-600 dark:text-gray-300" data-aos="fade-up">
          How We Work
        </h2>

        <div class="grid md:grid-cols-4 gap-6 text-sm">

          <div data-aos="fade-up">
            <h3 class="font-semibold">1. Discovery</h3>
            <p class="text-gray-500">Understand your goals</p>
          </div>

          <div data-aos="fade-up" data-aos-delay="100">
            <h3 class="font-semibold">2. Design</h3>
            <p class="text-gray-500">Craft user experience</p>
          </div>

          <div data-aos="fade-up" data-aos-delay="200">
            <h3 class="font-semibold">3. Build</h3>
            <p class="text-gray-500">Develop your system</p>
          </div>

          <div data-aos="fade-up" data-aos-delay="300">
            <h3 class="font-semibold">4. Launch</h3>
            <p class="text-gray-500">Deploy & support</p>
          </div>

        </div>

      </div>
    </section>

    <!-- WHY CHOOSE US -->
    <section class="py-20">
      <div class="max-w-6xl mx-auto px-6">

        <h2 class="text-3xl font-bold text-center mb-12" data-aos="fade-up">
          Why Choose FixKraft
        </h2>

        <div class="grid md:grid-cols-3 gap-6 text-center">

          <div data-aos="fade-up" class="p-6">
            <h3 class="font-semibold mb-2">⚡ Fast Delivery</h3>
            <p class="text-gray-500 text-sm">
              We build efficiently without compromising quality.
            </p>
          </div>

          <div data-aos="fade-up" data-aos-delay="100" class="p-6">
            <h3 class="font-semibold mb-2">🧠 Smart Systems</h3>
            <p class="text-gray-500 text-sm">
              Built with scalability and performance in mind.
            </p>
          </div>

          <div data-aos="fade-up" data-aos-delay="200" class="p-6">
            <h3 class="font-semibold mb-2">🎯 Business Focused</h3>
            <p class="text-gray-500 text-sm">
              Everything is aligned with your business goals.
            </p>
          </div>

        </div>

      </div>
    </section>

    <!-- CTA -->
    <section class="py-24 bg-black text-white text-center">
      <div data-aos="zoom-in">

        <h2 class="text-3xl font-bold mb-4">
          Ready to build your system?
        </h2>

        <p class="text-gray-300 mb-6">
          Let&apos;s turn your idea into a working product.
        </p>

        <!-- <button
          @click="$router.push('/contact')"
          class="bg-primary px-6 py-3 rounded-xl shadow-lg hover:scale-105 transition"
        >
          Start a Project
        </button> -->

        <base-button @click="$router.push('/contact')">
        Start a Project
      </base-button>

      </div>
    </section>

  </div>
</template>

<style>
/* FADE ANIMATION */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>