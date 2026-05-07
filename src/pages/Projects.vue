<script setup lang="ts">
import { useProjectsStore } from '@/stores/projects'
import { onMounted, ref } from 'vue'

// FILTER STATE
const activeFilter = ref('All')

// MOCK DATA (Replace with API later)
const store = useProjectsStore()

onMounted(() => {
  store.load()
})

// FILTER LOGIC
const filteredProjects = () => {
  if (activeFilter.value === 'All') return store.projects
  return store.projects.filter(p => p.category === activeFilter.value)
}
</script>

<template>
  <div class="bg-white min-h-screen">

    <!-- HERO -->
    <section class="py-20 bg-gradient-to-br from-secondary to-black text-white text-center">
      <div class="max-w-4xl mx-auto px-6">

        <h1 class="text-4xl font-bold mb-4">
          Our Work
        </h1>

        <p class="text-gray-300">
          A collection of systems, websites, and digital products we've built.
        </p>

      </div>
    </section>

    <!-- FILTERS -->
    <section class="py-10">
      <div class="max-w-7xl mx-auto px-6 flex justify-center gap-4">

        <button
          v-for="filter in ['All', 'Web', 'CMS']"
          :key="filter"
          @click="activeFilter = filter"
          class="px-4 py-2 rounded-lg text-sm transition"
          :class="activeFilter === filter
            ? 'bg-primary text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
        >
          {{ filter }}
        </button>

      </div>
    </section>

    <!-- PROJECT GRID -->
    <section class="pb-20">
      <div class="max-w-7xl mx-auto px-6">

        <div class="grid md:grid-cols-3 gap-6">

          <div
            v-for="project in filteredProjects()"
            :key="project.id"
            @click="$router.push(`/projects/${project.id}`)"
            class="cursor-pointer group bg-gray-100 rounded-2xl overflow-hidden"
          >

            <!-- IMAGE -->
            <div class="h-52 overflow-hidden">
              <img
                :src="project.image"
                class="w-full h-full object-cover group-hover:scale-110 transition duration-500"
              />
            </div>

            <!-- CONTENT -->
            <div class="p-4 space-y-2">

              <h3 class="font-semibold">
                {{ project.title }}
              </h3>

              <p class="text-sm text-gray-500">
                {{ project.category }}
              </p>

            </div>

          </div>

        </div>

      </div>
    </section>

  </div>
</template>