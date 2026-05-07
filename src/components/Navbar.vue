<script setup lang="ts">
import { useSiteConfig } from '@/stores/siteConfig'
import { useThemeStore } from '@/stores/theme'
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from './ui/BaseButton.vue'

const mobileOpen = ref(false)
const activeSection = ref('home')

const route = useRoute()
const router = useRouter()

// NAV LINKS
const links = [
  { name: 'Home', path: '/' },
  { name: 'Process', path: '/process' },
  { name: 'Services', path: '/services' },
  { name: 'Projects', path: '/projects' },
  { name: 'Contact', path: '/contact' }
]

// TOGGLE MENU
const toggleMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

// NAVIGATION
const handleNav = (link: any) => {
  mobileOpen.value = false
  if (route.path !== link.path) {
    router.push(link.path)
  }
}

// ACTIVE LINK
const isActive = (link: any) => {
  return route.path === link.path
}

// CONTACT CTA
const openContactPage = () => {
  router.push('/contact')
}

// SCROLL OBSERVER (optional)
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

onMounted(() => {
  if (route.path === '/') {
    setupObserver()
  }
})

watch(
  () => route.path,
  async (newPath) => {
    if (newPath === '/') {
      await nextTick()
      setupObserver()
    }
  }
)

// DYNAMIC LOGO
const logo = ref('/fix-kraft-icon-no-bg.svg')

onMounted(() => {
  const saved = localStorage.getItem('logo')
  if (saved) logo.value = saved
})

// THEME
const theme = useThemeStore()

const toggleDark = () => {
  theme.toggleDark()
}

const config = useSiteConfig()

</script>

<template>
  <nav class="sticky top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">

    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

      <!-- LEFT: LOGO -->
      <div class="flex items-center gap-3">
        <img :src="config.logo" alt="logo" class="h-12 w-auto object-contain" />
        <span class="text-xl font-bold text-primary hidden sm:block">
          FixKraft
        </span>
      </div>

      <!-- CENTER: DESKTOP NAV -->
      <div class="hidden md:flex items-center gap-2">
        <button
          v-for="link in config.navLinks"
          :key="link.name"
          @click="handleNav(link)"
          class="relative px-4 py-2 text-sm rounded-lg transition-all duration-300"
        >
          <!-- ACTIVE BACKGROUND -->
          <span
            v-if="isActive(link)"
            class="absolute inset-0 bg-primary/10 rounded-lg"
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

      <!-- RIGHT: ACTIONS -->
      <div class="flex items-center gap-2">

        <!-- THEME BUTTON -->
        <button
          @click="toggleDark"
          class="flex items-center justify-center w-10 h-10 rounded-lg border border-gray-200 hover:bg-gray-100 hover:shadow-md hover:scale-105 transition"
        >
          <span v-if="theme.dark">🌙</span>
          <span v-else>☀️</span>
        </button>

        <!-- CTA (desktop only) -->
        <!-- <button
          @click="openContactPage"
          class="hidden md:block bg-primary text-white px-4 py-2 rounded-lg shadow hover:scale-105 transition"
        >
          Start Project
        </button> -->

        <base-button @click="openContactPage" class="hidden md:block">
        Start Project
      </base-button>

        <!-- MOBILE MENU BUTTON -->
        <button
          @click="toggleMenu"
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition"
        >
          ☰
        </button>

      </div>
    </div>

    <!-- MOBILE MENU WITH ANIMATION -->
    <transition name="fade">
      <div
        v-if="mobileOpen"
        class="md:hidden px-6 pb-6 bg-white border-t border-gray-200"
      >
        <div class="flex flex-col gap-3 mt-4">

          <button
            v-for="link in config.navLinks"
            :key="link.name"
            @click="handleNav(link)"
            class="text-left px-4 py-2 rounded-lg transition"
            :class="isActive(link)
              ? 'bg-primary/10 text-primary font-semibold'
              : 'text-gray-600 hover:bg-gray-100'"
          >
            {{ link.name }}
          </button>

          <!-- <button
            @click="openContactPage"
            class="bg-primary text-white px-4 py-2 rounded-lg mt-2"
          >
            Start Project
          </button> -->

          <base-button @click="openContactPage">Start Project</base-button>

        </div>
      </div>
    </transition>

  </nav>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>