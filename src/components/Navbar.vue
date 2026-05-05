<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const mobileOpen = ref(false)
const activeSection = ref('home')

const route = useRoute()
const router = useRouter()

// NAV LINKS CONFIG
const links = [
  { name: 'Home', path: '/' },
  { name: 'Process', path: '/process' },
  { name: 'Services', path: '/services' },
  { name: 'Contact', path: '/contact' },
  { name: 'Projects', path: '/projects' }
]

// TOGGLE MOBILE MENU
const toggleMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

// SMART NAVIGATION
const handleNav = async (link: any) => {
  mobileOpen.value = false

  router.push(link.path)
}

// ACTIVE STATE
const isActive = (link: any) => {
    return route.path === link.path
}

// OBSERVER (TRACK SCROLL SECTIONS)
const setupObserver = () => {
  const sections = document.querySelectorAll('section')

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeSection.value = entry.target.id
        }
      })
    },
    { threshold: 0.6 }
  )

  sections.forEach((section) => observer.observe(section))
}

// INIT OBSERVER ON LOAD
onMounted(() => {
  if (route.path === '/') {
    setupObserver()
  }
})

// RE-INIT OBSERVER WHEN ROUTE CHANGES
watch(
  () => route.path,
  async (newPath) => {
    if (newPath === '/') {
      await nextTick()
      setupObserver()
    }
  }
)
</script>

<template>
  <nav class="sticky top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">

    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

      <!-- LOGO -->
      <div class="flex items-center gap-3">
        <img src="/fix-kraft-icon-no-bg.svg" alt="logo" class="h-12 w-auto object-contain" />
        <span class="text-xl font-bold text-primary hidden sm:block">
          FixKraft
        </span>
      </div>

      <!-- DESKTOP NAV -->
      <div class="hidden md:flex items-center gap-2">

        <button
          v-for="link in links"
          :key="link.name"
          @click="handleNav(link)"
          class="relative px-4 py-2 text-sm rounded-lg transition-all duration-300"
        >

          <!-- ACTIVE PILL -->
          <span
            v-if="isActive(link)"
            class="absolute inset-0 bg-primary/10 rounded-lg transition-all duration-300"
          ></span>

          <!-- TEXT -->
          <span
            :class="[
              'relative z-10 transition',
              isActive(link)
                ? 'text-primary font-semibold'
                : 'text-gray-600 hover:text-primary'
            ]"
          >
            {{ link.name }}
          </span>

        </button>

      </div>

      <!-- CTA -->
      <div class="hidden md:block">
        <button class="bg-primary text-white px-4 py-2 rounded-lg shadow hover:scale-105 transition">
          Start Project
        </button>
      </div>

      <!-- MOBILE MENU BUTTON -->
      <button
        @click="toggleMenu"
        class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition"
      >
        ☰
      </button>

    </div>

    <!-- MOBILE MENU -->
    <div
      v-if="mobileOpen"
      class="md:hidden px-6 pb-6 bg-white border-t border-gray-200"
    >
      <div class="flex flex-col gap-3 mt-4">

        <button
          v-for="link in links"
          :key="link.name"
          @click="handleNav(link)"
          class="text-left px-4 py-2 rounded-lg transition"
          :class="isActive(link)
            ? 'bg-primary/10 text-primary font-semibold'
            : 'text-gray-600 hover:bg-gray-100'"
        >
          {{ link.name }}
        </button>

        <button class="bg-primary text-white px-4 py-2 rounded-lg mt-2">
          Start Project
        </button>

      </div>
    </div>

  </nav>
</template>