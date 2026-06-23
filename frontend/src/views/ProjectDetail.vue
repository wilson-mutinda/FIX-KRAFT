<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue';
import { useProjectsStore } from '@/stores/projects';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const store = useProjectsStore()
const project = ref<any>(null)

onMounted(async () => {
  await store.load()
  project.value = store.projects.find(p => p.id === Number(route.params.id))
})

// Helper: split comma-separated strings into arrays, returning empty array if undefined/null
const splitList = (str: string | undefined | null): string[] => {
  if (!str) return []
  return str.split(',').map(s => s.trim()).filter(Boolean)
}

</script>

<template>
  <div v-if="project" class="bg-white dark:bg-gray-900">

    <!-- HERO -->
     <section class="relative py-20 bg-gradient-to-br from-secondary to-black text-white overflow-hidden">
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>

      <div class="relative z-10 max-w-5xl mx-auto px-6">
        <h1 class="text-4xl md:text-5xl font-bold mb-2">{{ project.title }}</h1>
        <p class="text-gray-300 text-lg max-w-2xl">{{ project.description || project.overview || '' }}</p>
        <div class="mt-4 flex flex-wrap gap-2">
          <span v-for="tech in splitList(project.technologies)" :key="tech" class="bg-white/10 px-3 py-1 rounded-full text-sm">{{ tech }}</span>
        </div>
        <div class="mt-6 flex flex-wrap gap-4">
          <a v-if="project.project_url" :href="project.project_url" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline inline-flex items-center gap-1">🔗 Live Demo</a>
          <a v-if="project.github_url" :href="project.github_url" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline inline-flex items-center gap-1">💻 Source</a>
        </div>

        <!-- Status badge -->
         <span class="inline-block mt-4 px-3 py-1 rounded-full text-xs font-medium" :class="{
          'bg-yellow-100 text-yellow-800': project.status === 'planning',
          'bg-blue-100 text-blue-800': project.status === 'in_progress',
          'bg-green-100 text-green-800': project.status === 'launched',
          'bg-gray-100 text-gray-800': project.status === 'maintainance'
         }">
          {{ project.status.replace('_', ' ').toUpperCase() }}
         </span>
      </div>
     </section>

     <!-- HERO IMAGE (fallback to project.image) -->
      <div class="max-w-4xl mx-auto px-6 -mt-8 relative z-10">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden">
          <img
          :src="project.hero_image || project.image || 'https://via.placeholder.com/1200x600?text=Project'" 
          class="w-full object-cover max-h-56 md:max-h-72" 
          :alt="project.title"
          >
        </div>
      </div>

      <!-- CASE STUDY CONTENT (optional) -->
      <section class="py-20 max-w-4xl mx-auto px-6 space-y-12">
        <div v-if="project.overview" data-aos="fade-up">
          <h2 class="text-2xl font-bold mb-3">Overview</h2>
          <p class="text-gray-600 dark:text-gray-300">{{ project.overview }}</p>
        </div>
        <div v-if="project.problem" data-aos="fade-up">
          <h2 class="text-2xl font-bold mb-3">Problem</h2>
          <p class="text-gray-600 dark:text-gray-300">{{ project.problem }}</p>
        </div>
        <div v-if="project.solution" data-aos="fade-up">
          <h2 class="text-2xl font-bold mb-3">Solution</h2>
          <p class="text-gray-600 dark:text-gray-300">{{ project.solution }}</p>
        </div>
      </section>

       <!-- RESULTS (if any) -->
      <section v-if="splitList(project.results).length" class="py-20 bg-gray-50 dark:bg-gray-800 text-center">
        <div class="max-w-5xl mx-auto px-6">
          <h2 class="text-3xl font-bold mb-10">Results & Impact</h2>
          <div class="grid md:grid-cols-3 gap-6">
            <div v-for="r in splitList(project.results)" :key="r"
                class="bg-white dark:bg-gray-900 p-6 rounded-xl shadow hover:-translate-y-2 transition">
              {{ r }}
            </div>
          </div>
        </div>
      </section>

        <!-- FEATURES (if any) -->
      <section v-if="splitList(project.features).length" class="py-20 max-w-5xl mx-auto px-6">
        <h2 class="text-3xl font-bold mb-10 text-center">Key Features</h2>
        <div class="grid md:grid-cols-2 gap-6">
          <div v-for="f in splitList(project.features)" :key="f"
              class="p-5 border rounded-xl dark:border-gray-700 hover:shadow-md transition">
            {{ f }}
          </div>
        </div>
      </section>

         <!-- TECH STACK (if separate from technologies) -->
      <section v-if="splitList(project.tech_stack).length" class="pb-20 text-center">
        <h2 class="text-2xl font-bold mb-6">Tech Stack</h2>
        <div class="flex flex-wrap justify-center gap-3">
          <span v-for="tech in splitList(project.tech_stack)" :key="tech"
                class="px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-full text-sm">
            {{ tech }}
          </span>
        </div>
      </section>

          <!-- GALLERY (if any) -->
      <section v-if="splitList(project.gallery).length" class="pb-20 max-w-6xl mx-auto px-6">
        <h2 class="text-2xl font-bold mb-6">Preview</h2>
        <div class="grid md:grid-cols-2 gap-6">
          <img v-for="img in splitList(project.gallery)" :key="img"
              :src="img" class="rounded-xl shadow hover:scale-105 transition" />
        </div>
      </section>

           <!-- FINAL CTA -->
            <section class="py-24 bg-black text-white text-center">
              <div class="max-w-3xl mx-auto px-6" data-aos="zoom-in">
                <h2 class="text-3xl font-bold mb-4">Want something like this?</h2>
                <p class="text-gray-300 mb-6">Let's build your system next.</p>
                <BaseButton @click="$router.push('/contact')" class="shadow-lg hover:scale-105 transition">
                  Start a Project
                </BaseButton>
              </div>
            </section>
  </div>
  <div v-else class="text-center py-20">
    <p class="text-gray-500">Loading project...</p>
  </div>
</template>
