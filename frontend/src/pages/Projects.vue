<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue';
import { useProjectsStore } from '@/stores/projects';

const store = useProjectsStore()

</script>

<template>
  <div class="bg-white dark:bg-gray-900 min-h-screen">

    <!-- HERO -->
     <section class="relative py-24 bg-gradient-to-br from-secondary to-black text-white text-center overflow-hidden">
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-primary/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      <div class="relative z-10 max-w-4xl mx-auto px-6" data-aos="fade-up">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Our Work</h1>
        <p class="text-gray-300 text-lg max-w-2xl mx-auto">A collection of systems, websites, and digital products we've built.</p>
      </div>
     </section>

     <!-- PROJECTS GRID -->
      <section class="py-20 bg-gray-50 dark:bg-gray-800">
        <div class="max-w-7xl mx-auto px-6">
          <div v-if="store.loading" class="text-center py-12">
            <div class="inline-block w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            <p class="text-gray-500 mt-4">Loading projects...</p>
          </div>

          <div v-else-if="store.projects.length === 0" class="text-center py-12">
            <p class="text-gray-500">No projects yet.</p>
          </div>

          <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div
             v-for="project in store.projects" 
             :key="project.id" 
             data-aos="fade-up" 
             class="group bg-white dark:bg-gray-900 rounded-2xl shadow-sm hover:shadow-xl transition duration-300 overflow-hidden flex flex-col"
            >

              <div class="relative overflow-hidden">
                <img
                 :src="project.image || 'https://via.placeholder.com/600x400?text=Project'" 
                 class="w-full h-56 object-cover group-hover:scale-105 transition duration-500" :alt="project.title" 
                />
                <div class="absolute inset-0 bg-primary/0 group-hover:bg-primary/10 transition"></div>
              </div>

              <div class="p-6 flex-1 flex flex-col">
                <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-2">{{ project.title }}</h3>
                <p class="text-gray-600 dark:text-gray-300 text-sm flex-1 mb-4">{{ project.description }}</p>

                <!-- Technologies as badges -->
                 <div class="flex flex-wrap gap-2 mb-4">
                  <span
                   v-for="tech in (project.technologies || '').split(',').map(t => t.trim())" 
                   :key="tech" 
                   class="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs px-3 py-1 rounded-full"
                  >
                    {{ tech }}
                  </span>
                 </div>

                 <!-- Links (projects_url and github_url) -->
                  <div class="flex gap-2 mb-4">
                    <a
                     v-if="project.project_url" 
                     :href="project.project_url" 
                     target="_blank" 
                     rel="noopener noreferrer"
                    >
                      🔗 Live Demo
                    </a>
                    <a
                     v-if="project.github_url" 
                     :href="project.github_url" 
                     target="_blank" 
                     rel="noopener noreferrer">
                      💻 Source
                    </a>
                  </div>

                  <!-- BaseButton -->
                   <BaseButton
                    @click="$router.push(`/projects/${project.id}`)" 
                    class="w-full text-center justify-center"
                  >
                    View Details  →
                  </BaseButton>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
       <section class="py-24 bg-gradient-to-r from-secondary to-black text-white text-center">
        <div class="max-w-3xl mx-auto px-6" data-aos="zoom-in">
          <h2 class="text-3xl font-bold mb-4">Have a Project in Mind?</h2>
          <p class="text-gray-300 mb-6">Let's discuss how we can bring your idea to life.</p>
          <BaseButton @click="$router.push('/contact')" class="shadow-lg hover:scale-105 transition">
            Start a Project
          </BaseButton>
        </div>
       </section>
  </div>
</template>