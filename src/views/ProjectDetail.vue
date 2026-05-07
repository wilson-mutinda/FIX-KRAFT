<script setup lang="ts">
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useProjectsStore } from '@/stores/projects';

const route = useRoute()

const store = useProjectsStore()

const project = ref<any>(null)

onMounted(() => {
  store.load()
  project.value = store.getById(Number(route.params.id))
})

</script>

<template>
  <div class="bg-white">

    <!-- HERO -->
    <section class="py-20 bg-gradient-to-br from-secondary to-black text-white">
      <div class="max-w-5xl mx-auto px-6" data-aos="fade-up">

        <h1 class="text-4xl font-bold mb-4">
          {{ project.title }}
        </h1>

        <p class="text-gray-300">
          {{ project.category }}
        </p>

      </div>
    </section>

    <!-- HERO IMAGE -->
    <div class="max-w-6xl mx-auto px-6 -mt-10" data-aos="zoom-in">
      <img :src="project.heroImage" class="rounded-2xl shadow-xl" />
    </div>

    <!-- OVERVIEW -->
    <section class="py-20">
      <div class="max-w-4xl mx-auto px-6 space-y-12">

        <div data-aos="fade-up">
          <h2 class="text-2xl font-bold mb-3">Overview</h2>
          <p class="text-gray-600">{{ project.overview }}</p>
        </div>

        <div data-aos="fade-up">
          <h2 class="text-2xl font-bold mb-3">Problem</h2>
          <p class="text-gray-600">{{ project.problem }}</p>
        </div>

        <div data-aos="fade-up">
          <h2 class="text-2xl font-bold mb-3">Solution</h2>
          <p class="text-gray-600">{{ project.solution }}</p>
        </div>

      </div>
    </section>

    <!-- RESULTS (THIS SELLS YOU) -->
    <section class="py-20 bg-gray-50 text-center">
      <div class="max-w-5xl mx-auto px-6">

        <h2 class="text-3xl font-bold mb-10" data-aos="fade-up">
          Results & Impact
        </h2>

        <div class="grid md:grid-cols-3 gap-6">

          <div
            v-for="r in project.results"
            :key="r"
            data-aos="zoom-in"
            class="p-6 bg-white rounded-xl shadow hover:-translate-y-2 transition"
          >
            {{ r }}
          </div>

        </div>

      </div>
    </section>

    <!-- FEATURES -->
    <section class="py-20">
      <div class="max-w-5xl mx-auto px-6">

        <h2 class="text-3xl font-bold mb-10 text-center" data-aos="fade-up">
          Key Features
        </h2>

        <div class="grid md:grid-cols-2 gap-6">

          <div
            v-for="f in project.features"
            :key="f"
            data-aos="fade-up"
            class="p-5 border rounded-xl hover:shadow-md transition"
          >
            {{ f }}
          </div>

        </div>

      </div>
    </section>

    <!-- TECH STACK -->
    <section class="pb-20 text-center">
      <h2 class="text-2xl font-bold mb-6" data-aos="fade-up">
        Tech Stack
      </h2>

      <div class="flex flex-wrap justify-center gap-3">
        <span
          v-for="tech in project.tech"
          :key="tech"
          class="px-4 py-2 bg-gray-100 rounded-full text-sm"
        >
          {{ tech }}
        </span>
      </div>
    </section>

    <!-- GALLERY -->
    <section class="pb-20">
      <div class="max-w-6xl mx-auto px-6">

        <h2 class="text-2xl font-bold mb-6" data-aos="fade-up">
          Preview
        </h2>

        <div class="grid md:grid-cols-2 gap-6">

          <img
            v-for="img in project.gallery"
            :key="img"
            :src="img"
            data-aos="zoom-in"
            class="rounded-xl shadow hover:scale-105 transition"
          />

        </div>

      </div>
    </section>

    <!-- CTA (VERY IMPORTANT) -->
    <section class="py-24 bg-black text-white text-center">
      <div data-aos="zoom-in">

        <h2 class="text-3xl font-bold mb-4">
          Want something like this?
        </h2>

        <p class="text-gray-300 mb-6">
          Let&apos;s build your system next.
        </p>

        <button
          @click="$router.push('/contact')"
          class="bg-primary px-6 py-3 rounded-xl hover:scale-105 transition"
        >
          Start a Project
        </button>

      </div>
    </section>

  </div>
</template>