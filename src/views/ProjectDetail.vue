<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const projectId = route.params.id

// MOCK DATA (replace with API later)
const project = ref({
  title: 'SaaS Dashboard System',
  category: 'Web Application',
  heroImage: 'https://via.placeholder.com/1200x600',

  overview:
    'A full-featured SaaS dashboard designed for managing users, analytics, and business operations.',

  problem:
    'The client lacked a centralized system to manage users and track performance metrics efficiently.',

  solution:
    'We built a scalable dashboard with real-time analytics, role-based access, and modern UI.',

  tech: ['Vue', 'Django', 'PostgreSQL', 'Tailwind'],

  gallery: [
    'https://via.placeholder.com/800x500',
    'https://via.placeholder.com/800x500',
    'https://via.placeholder.com/800x500'
  ]
})
</script>

<template>
  <div class="bg-white">

    <!-- HERO -->
    <section class="py-20 bg-gradient-to-br from-secondary to-black text-white">
      <div class="max-w-5xl mx-auto px-6">

        <h1 class="text-4xl font-bold mb-4">
          {{ project.title }}
        </h1>

        <p class="text-gray-300">
          {{ project.category }}
        </p>

      </div>
    </section>

    <!-- HERO IMAGE -->
    <div class="max-w-6xl mx-auto px-6 -mt-10">
      <img
        :src="project.heroImage"
        class="rounded-2xl shadow-xl"
      />
    </div>

    <!-- OVERVIEW -->
    <section class="py-20">
      <div class="max-w-4xl mx-auto px-6 space-y-10">

        <div>
          <h2 class="text-2xl font-bold mb-3">Overview</h2>
          <p class="text-gray-600">{{ project.overview }}</p>
        </div>

        <div>
          <h2 class="text-2xl font-bold mb-3">Problem</h2>
          <p class="text-gray-600">{{ project.problem }}</p>
        </div>

        <div>
          <h2 class="text-2xl font-bold mb-3">Solution</h2>
          <p class="text-gray-600">{{ project.solution }}</p>
        </div>

        <!-- TECH STACK -->
        <div>
          <h2 class="text-2xl font-bold mb-3">Tech Stack</h2>

          <div class="flex flex-wrap gap-2">
            <span
              v-for="tech in project.tech"
              :key="tech"
              class="px-3 py-1 bg-gray-100 rounded-full text-sm"
            >
              {{ tech }}
            </span>
          </div>
        </div>

      </div>
    </section>

    <!-- GALLERY -->
    <section class="pb-20">
      <div class="max-w-6xl mx-auto px-6">

        <h2 class="text-2xl font-bold mb-6">Preview</h2>

        <div class="grid md:grid-cols-2 gap-6">

          <img
            v-for="img in project.gallery"
            :key="img"
            :src="img"
            class="rounded-xl shadow hover:scale-105 transition"
          />

        </div>

      </div>
    </section>

  </div>
</template>
