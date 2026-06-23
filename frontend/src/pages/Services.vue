<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import { useServicesStore } from '@/stores/services'
import { onMounted } from 'vue'

const store = useServicesStore()

// Helper to convert comma-separateed string to array
const getFeatureList = (features: string) => {
  if (!features) return []
  return features.split(',').map(f => f.trim())
}

onMounted(() => {
  store.load()
})

</script>

<template>
  <div class="bg-white dark:bg-gray-900">

    <!-- HERO with subtle animation -->
    <section class="relative py-24 bg-gradient-to-br from-secondary to-black text-white text-center overflow-hidden">
      <!-- Background glow  -->
       <div class="absolute -top-24 -right-24 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
       <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>

      <div class="relative z-10 max-w-4xl mx-auto px-6" data-aos="fade-up">

        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          Services That Build
          <span class="text-primary">Real Products</span>
        </h1>

        <p class="text-gray-300 text-lg mb-6 max-w-2xl mx-auto">
          We don&apos;t just design — we engineer scalable digital systems for modern businesses.
        </p>

        <base-button @click="$router.push('/contact')">
        Start Your Project
      </base-button>

      </div>
    </section>

    <!-- SERVICES -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-800 dark:text-white">What We Offer</h2>
          <p class="text-gray-500 dark:text-gray-400 max-w-2xl mx-auto mt-4">
            Explore our full range of digital solutions designed to grow your business.
          </p>
        </div>

        <div v-if="store.loading" class="text-center py-12">
          <div class="inline-block w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
          <p class="text-gray-500 mt-4">Loading services...</p>
        </div>

        <div v-else-if="store.services.length === 0" class="text-center py-12">
          <p class="text-gray-500">No services available yet.</p>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="service in store.services" :key="service.id"
               data-aos="fade-up"
               class="group bg-white dark:bg-gray-900 rounded-2xl shadow-sm hover:shadow-xl transition duration-300 overflow-hidden flex flex-col">

            <div class="relative overflow-hidden">
              <img :src="service.image || 'https://via.placeholder.com/600x400?text=Service'"
                   class="w-full h-52 object-cover group-hover:scale-105 transition duration-500"
                   :alt="service.title" />
              <div class="absolute inset-0 bg-primary/0 group-hover:bg-primary/10 transition"></div>
            </div>

            <div class="p-6 flex-1 flex flex-col">
              <h3 class="text-xl font-bold mb-2 text-gray-800 dark:text-white">{{ service.title }}</h3>
              <p class="text-gray-600 dark:text-gray-300 text-sm mb-4 flex-1">{{ service.description }}</p>

              <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 mb-6">
                <li v-for="feature in getFeatureList(service.features)" :key="feature" class="flex items-start gap-2">
                  <span class="text-primary font-bold">✓</span>
                  <span>{{ feature }}</span>
                </li>
              </ul>

              <BaseButton @click="$router.push('/contact')" class="w-full text-center justify-center">
                Enquire Now →
              </BaseButton>
            </div>
          </div>
        </div>
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

    <!-- WHY CHOOSE US (with icons) -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-6xl mx-auto px-6">
        <h2 class="text-3xl font-bold text-center mb-12 text-gray-800 dark:text-white">Why Choose FixKraft</h2>
        <div class="grid md:grid-cols-3 gap-8 text-center">
          <div data-aos="fade-up" class="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-sm hover:shadow-md transition">
            <div class="text-4xl mb-4">⚡</div>
            <h3 class="font-semibold mb-2">Fast Delivery</h3>
            <p class="text-gray-500 text-sm">We build efficiently without compromising quality.</p>
          </div>
          <div data-aos="fade-up" data-aos-delay="100" class="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-sm hover:shadow-md transition">
            <div class="text-4xl mb-4">🧠</div>
            <h3 class="font-semibold mb-2">Smart Systems</h3>
            <p class="text-gray-500 text-sm">Built with scalability and performance in mind.</p>
          </div>
          <div data-aos="fade-up" data-aos-delay="200" class="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-sm hover:shadow-md transition">
            <div class="text-4xl mb-4">🎯</div>
            <h3 class="font-semibold mb-2">Business Focused</h3>
            <p class="text-gray-500 text-sm">Everything is aligned with your business goals.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FINAL CTA -->
    <section class="py-24 bg-gradient-to-r from-secondary to-black text-white text-center">
      <div class="max-w-3xl mx-auto px-6" data-aos="zoom-in">
        <h2 class="text-3xl font-bold mb-4">Ready to Build Your System?</h2>
        <p class="text-gray-300 mb-6">Let&apos;s turn your idea into a working product.</p>
        <BaseButton @click="$router.push('/contact')" class="shadow-lg hover:scale-105 transition">
          Start a Project
        </BaseButton>
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