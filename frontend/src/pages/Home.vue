<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue';
import { useProjectsStore } from '@/stores/projects';
import { useServicesStore } from '@/stores/services';
import { useTestimonialStore } from '@/stores/testimonials';
import { onMounted, onUnmounted } from 'vue';

const testimonialStore = useTestimonialStore();
const servicesStore = useServicesStore();
const projectsStore = useProjectsStore();

let interval: number;

// Safe helper to extract hostname from URL
const getHostname = (url: string) => {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

onMounted(() => {
  testimonialStore.load();
  servicesStore.load();
  projectsStore.load();

  // Poll every 30 seconds to keep testimonialsup-to-date
  interval = setInterval(() => {
    testimonialStore.load();
  }, 30000);
});

onUnmounted(() => {
  clearInterval(interval);
});

</script>

<template>
  <div>

    <!-- HERO – stronger value proposition + new CTA -->
    <section class="relative bg-gradient-to-br from-secondary via-[#001f33] to-black text-white py-24 overflow-hidden">
      <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">

        <!-- TEXT -->
        <div data-aos="fade-right" class="space-y-6">
          <h1 class="text-4xl md:text-5xl font-bold leading-tight">
            We Build Digital Products That <span class="text-primary">Grow Your Business</span><br />
            – Websites, SaaS, and Custom Systems
          </h1>

          <p class="text-gray-300 text-lg">
            From concept to launch – we create scalable, high‑performance solutions tailored to your needs.
          </p>

          <div class="flex flex-wrap gap-4">
            <BaseButton @click="$router.push('/contact')">
              Get Free Consultation
            </BaseButton>

            <button
              @click="$router.push('/projects')"
              class="border border-white/20 px-6 py-3 rounded-xl hover:bg-white/10 transition"
            >
              View Our Work
            </button>
          </div>
        </div>

        <!-- IMAGE MOCKUP -->
        <div data-aos="fade-left" class="relative">
          <div class="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 shadow-2xl">
            <img
              src="https://images.pexels.com/photos/5716032/pexels-photo-5716032.jpeg"
              class="rounded-xl object-cover w-full h-64"
              alt="Digital product development"
            />
          </div>
        </div>

      </div>
    </section>

    <!-- RESULTS / TRUST BAR (numbers) -->
    <section class="py-12 bg-white dark:bg-gray-900 border-y border-gray-100 dark:border-gray-800">
      <div class="max-w-5xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
        <div>
          <p class="text-3xl font-bold text-primary">20+</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">Projects Delivered</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-primary">100%</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">Client Satisfaction</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-primary">4.9★</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">Average Rating</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-primary">50+</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">Happy Clients</p>
        </div>
      </div>
    </section>

    <!-- SERVICES (enhanced with short benefit descriptions) -->
    <section class="py-20 bg-gray-50 dark:bg-gray-900 text-center">
      <h2 class="text-3xl font-bold mb-4" data-aos="fade-up">What We Do</h2>
      <p class="text-gray-500 dark:text-gray-400 mb-12 max-w-2xl mx-auto" data-aos="fade-up">
        We build digital products that solve real business problems and deliver measurable results.
      </p>

      <div v-if="servicesStore.loading" class="py-12">
        <p class="text-gray-500">Loading services...</p>
      </div>
      <div v-else-if="servicesStore.services.length === 0" class="py-12">
        <p class="text-gray-500">No services yet.</p>
      </div>
      <!-- Show only first 3 services (or a slice) -->
      <div v-else class="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto px-6">
        <div
         v-for="service in servicesStore.services.slice(0, 3)" 
         :key="service.id" 
         data-aos="zoom-in" 
         class="p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-2 transition-all duration-300"
        >
          <img
           :src="service.image || 'https://via.placeholder.com/400x200?text=Service'" 
           class="h-32 w-full object-cover rounded-lg mb-4" :alt="service.title"
         />
          <h3 class="font-semibold mb-1">{{ service.title }}</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ service.description }}</p>
        </div>
      </div>

      <BaseButton @click="$router.push('/services')" data-aos="fade-up" class="mt-10">
        View All Services
      </BaseButton>
    </section>

    <!-- HOW IT WORKS (new) -->
    <section class="py-16 bg-white dark:bg-gray-900">
      <h2 class="text-3xl font-bold text-center mb-12" data-aos="fade-up">How We Work</h2>
      <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto px-6 text-center">
        <div data-aos="fade-up">
          <div class="text-4xl mb-3">📋</div>
          <h3 class="font-semibold">1. Discovery</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">We understand your goals, challenges, and users.</p>
        </div>
        <div data-aos="fade-up" data-aos-delay="100">
          <div class="text-4xl mb-3">🎨</div>
          <h3 class="font-semibold">2. Design & Build</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">We design, develop, and iterate until it's right.</p>
        </div>
        <div data-aos="fade-up" data-aos-delay="200">
          <div class="text-4xl mb-3">🚀</div>
          <h3 class="font-semibold">3. Launch & Support</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">We deploy your product and provide ongoing support.</p>
        </div>
      </div>
    </section>

    <!-- DYNAMIC TESTIMONIALS SECTION -->
     <section class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-5xl mx-auto px-6">
        <h2 class="text-3xl font-bold text-center mb-12">What Our Clients Say</h2>

        <!-- Loading state -->
         <div v-if="testimonialStore.loading" class="text-center py-12">
          <p class="text-gray-500">Loading testimonials...</p>
         </div>

         <!-- Empty state -->
          <div v-else-if="testimonialStore.testimonials.length === 0" class="text-center py-12">
            <p class="text-gray-500">No testimonials yet.</p>
          </div>

          <!-- Testimonials grid -->
           <div v-else class="grid md:grid-cols-2 gap-8">
            <div v-for="item in testimonialStore.testimonials" :key="item.id" class="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow" data-aos="fade-up">
              <div class="flex items-center gap-4 mb-4">
                <!-- Clickable logo -->
                 <a v-if="item.website_url" :href="item.website_url" target="_blank" rel="noopener noreferrer" class="block">
                  <img :src="item.logo || 'https://via.placeholder.com/80x80?text=' + encodeURIComponent(item.client_name)" :alt="item.client_name" class="w-20 h-20 object-contain rounded-full border border-gray-200 dark:border-gray-700 hover:opacity-80 transition">
                 </a>
                 <div v-else class="">
                  <img :src="item.logo || 'https://via.placeholder.com/80x80?text=' + encodeURIComponent(item.client_name)" :alt="item.client_name" class="w-20 h-20 object-contain rounded-full border border-gray-200 dark:border-gray-700">
                 </div>
                 <div class="">
                  <p class="font-semibold">{{ item.client_name }}</p>
                  <p class="text-sm text-gray-500">{{ item.client_role }}</p>
                  <a v-if="item.website_url" :href="item.website_url" target="_blank" rel="noopener noreferrer" class="text-primary text-sm hover:underline">{{ getHostname(item.website_url) }}</a>
                 </div>
              </div>
              <p class="text-gray-600 dark:text-gray-300 italic">{{ item.testimonial_text }}</p>
            </div>
           </div>
      </div>
     </section>

    <!-- PROJECTS (existing – unchanged, but you can link to detail pages later) -->
    <section class="py-20 bg-white dark:bg-gray-900 text-center">
      <h2 class="text-3xl font-bold mb-12" data-aos="fade-up">Selected Work</h2>

      <div v-if="projectsStore.loading" class="py-12">
        <p class="text-gray-500">Loading Projects...</p>
      </div>
      <div v-else-if="projectsStore.projects.length === 0" class="py-12">
        <p class="text-gray-500">No projects yet.</p>
      </div>
      <div v-else class="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto px-6">
        <div v-for="project in projectsStore.projects.slice(0, 3)" :key="project.id" class="group rounded-2xl bg-white dark:bg-gray-800 overflow-hidden shadow-sm hover:shadow-xl transition">
          <img
           :src="project.image || 'https://via.placeholder.com/600x400?text=Project'" 
           class="h-56 w-full object-cover group-hover:scale-110 transition duration-500" 
           :alt="project.title" 
          />
          <div class="p-4 text-left">
            <h3 class="font-semibold">{{ project.title }}</h3>
            <p class="text-sm text-gray-500">{{ project.technologies || 'Project' }}</p>
          </div>
        </div>
      </div>

      <BaseButton @click="$router.push('/projects')" class="mt-10">
        View All Projects
      </BaseButton>
    </section>

    <!-- FINAL CTA – stronger copy -->
    <section class="py-24 bg-gradient-to-r from-secondary to-black text-white text-center">
      <div class="max-w-3xl mx-auto px-6" data-aos="zoom-in">
        <h2 class="text-3xl font-bold mb-4">Ready to Build Your Digital Product?</h2>
        <p class="text-gray-300 mb-6">Let's talk about your idea and turn it into a scalable solution.</p>
        <BaseButton @click="$router.push('/contact')">
          Book a Free Consultation
        </BaseButton>
      </div>
    </section>

  </div>
</template>