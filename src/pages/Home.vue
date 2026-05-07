<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue';

</script>

<template>
  <div>

    <!-- HERO -->
    <section class="relative bg-gradient-to-br from-secondary via-[#001f33] to-black text-white py-24 overflow-hidden">
      <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">

        <!-- TEXT -->
        <div data-aos="fade-right" class="space-y-6">

          <h1 class="text-4xl md:text-5xl font-bold leading-tight">
            We Design & Build
            <span class="text-primary">High-Performance</span><br />
            Digital Products
          </h1>

          <p class="text-gray-300 text-lg">
            Websites, SaaS dashboards, and custom CMS systems tailored for modern businesses.
          </p>

          <div class="flex gap-4">
            <!-- <button
              @click="$router.push('/contact')"
              class="bg-primary px-6 py-3 rounded-xl shadow-lg 
              hover:scale-105 hover:shadow-xl active:scale-95 transition-all duration-300"
            >
              Start Project
            </button> -->

            <BaseButton @click="$router.push('/contact')">
              Start Project
            </BaseButton>

            <button
              @click="$router.push('/projects')"
              class="border border-white/20 px-6 py-3 rounded-xl 
              hover:bg-white/10 transition"
            >
              View Work
            </button>
          </div>

        </div>

        <!-- IMAGE MOCKUP -->
        <div data-aos="fade-left" class="relative">
          <div class="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 shadow-2xl">
            <img
              src="https://images.pexels.com/photos/5716032/pexels-photo-5716032.jpeg"
              class="rounded-xl object-cover w-full h-64"
            />
          </div>
        </div>

      </div>
    </section>

    <!-- TRUST -->
    <section class="py-16 bg-surface text-center">
      <div class="max-w-5xl mx-auto px-6" data-aos="fade-up">
        <p class="text-gray-500 text-sm mb-6 uppercase tracking-wide">
          Trusted Tools & Technologies
        </p>

        <div class="flex flex-wrap justify-center gap-6 text-gray-400">
          <span>Django</span>
          <span>Vue</span>
          <span>PostgreSQL</span>
          <span>Tailwind</span>
        </div>
      </div>
    </section>

    <!-- SERVICES -->
    <section class="py-20 bg-gray-50 text-center">
      <h2 class="text-3xl font-bold mb-12" data-aos="fade-up">
        What We Do
      </h2>

      <div class="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto px-6">

        <div data-aos="zoom-in"
          class="p-6 bg-white rounded-2xl shadow-sm 
          hover:shadow-xl hover:-translate-y-2 transition-all duration-300">

          <img src="https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg"
               class="h-32 w-full object-cover rounded-lg mb-4"/>

          <h3 class="font-semibold mb-2">Web Development</h3>
          <p class="text-sm text-gray-500">Modern, responsive websites</p>
        </div>

        <div data-aos="zoom-in" data-aos-delay="100"
          class="p-6 bg-white rounded-2xl shadow-sm 
          hover:shadow-xl hover:-translate-y-2 transition-all duration-300">

          <img src="https://images.pexels.com/photos/3861958/pexels-photo-3861958.jpeg"
               class="h-32 w-full object-cover rounded-lg mb-4"/>

          <h3 class="font-semibold mb-2">SaaS Systems</h3>
          <p class="text-sm text-gray-500">Scalable dashboards & apps</p>
        </div>

        <div data-aos="zoom-in" data-aos-delay="200"
          class="p-6 bg-white rounded-2xl shadow-sm 
          hover:shadow-xl hover:-translate-y-2 transition-all duration-300">

          <img src="https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg"
               class="h-32 w-full object-cover rounded-lg mb-4"/>

          <h3 class="font-semibold mb-2">Custom CMS</h3>
          <p class="text-sm text-gray-500">Manage content easily</p>
        </div>

      </div>

      <!-- <button
        data-aos="fade-up"
        @click="$router.push('/services')"
        class="mt-10 bg-primary text-white px-6 py-3 rounded-lg 
        hover:scale-105 transition"
      >
        View All Services
      </button> -->

      <BaseButton @click="$router.push('/services')" data-aos="fade-up" class="mt-10">
        View All Services
      </BaseButton>
    </section>

    <!-- PROJECTS -->
    <section class="py-20 bg-white text-center">
      <h2 class="text-3xl font-bold mb-12" data-aos="fade-up">
        Selected Work
      </h2>

      <div class="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto px-6">

        <div data-aos="fade-up"
          class="group rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition">

          <img src="https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg"
               class="h-56 w-full object-cover group-hover:scale-110 transition duration-500"/>

          <div class="p-4 text-left">
            <h3 class="font-semibold">SaaS Dashboard</h3>
            <p class="text-sm text-gray-500">Admin system</p>
          </div>
        </div>

        <div data-aos="fade-up" data-aos-delay="100"
          class="group rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition">

          <img src="https://images.pexels.com/photos/3182773/pexels-photo-3182773.jpeg"
               class="h-56 w-full object-cover group-hover:scale-110 transition duration-500"/>

          <div class="p-4 text-left">
            <h3 class="font-semibold">School CMS</h3>
            <p class="text-sm text-gray-500">Education system</p>
          </div>
        </div>

        <div data-aos="fade-up" data-aos-delay="200"
          class="group rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition">

          <img src="https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg"
               class="h-56 w-full object-cover group-hover:scale-110 transition duration-500"/>

          <div class="p-4 text-left">
            <h3 class="font-semibold">Portfolio</h3>
            <p class="text-sm text-gray-500">Personal brand</p>
          </div>
        </div>

      </div>

      <!-- <button
        data-aos="fade-up"
        @click="$router.push('/projects')"
        class="mt-10 bg-primary text-white px-6 py-3 rounded-lg 
        hover:scale-105 transition"
      >
        View All Projects
      </button> -->

      <BaseButton data-aos="fade-up" @click="$router.push('/projects')" class="mt-10">
        View All Projects
      </BaseButton>
    </section>

    <!-- CTA -->
    <section class="py-24 bg-gradient-to-r from-secondary to-black text-white text-center">
      <div class="max-w-3xl mx-auto px-6" data-aos="zoom-in">

        <h2 class="text-3xl font-bold mb-4">
          Ready to build something powerful?
        </h2>

        <p class="text-gray-300 mb-6">
          Let&apos;s turn your idea into a scalable digital product.
        </p>

        <!-- <button
          @click="$router.push('/contact')"
          class="bg-primary px-6 py-3 rounded-xl shadow-lg 
          hover:scale-105 transition"
        >
          Start a Project
        </button> -->

        <BaseButton @click="$router.push('/contact')" class="">
          start a Project
        </BaseButton>

      </div>
    </section>

  </div>
</template>