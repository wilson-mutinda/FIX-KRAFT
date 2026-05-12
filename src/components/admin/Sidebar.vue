<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router'

defineProps<{
  open: boolean
}>()

const router = useRouter()

const links = [
  { name: 'Dashboard', path: '/admin' },
  { name: 'Projects', path: '/admin/projects' },
  { name: 'Services', path: '/admin/services' },
  { name: 'Messages', path: '/admin/messages' },
  { name: 'Settings', path: '/admin/settings' },
  { name: 'Media', path: '/admin/media' }
]

const auth = useAuthStore()

const handleLogout = () => {

  auth.logout()

  router.push('/login')
}
</script>

<template>
  <aside
    :class="[
      'bg-white border-r border-gray-200 h-full transition-all duration-300',
      open ? 'w-64' : 'w-20'
    ]"
  >

    <!-- LOGO -->
    <div class="h-16 flex items-center justify-center border-b">
      <span class="font-bold text-primary">
        {{ open ? 'FixKraft' : 'FK' }}
      </span>
    </div>

    <!-- LINKS -->
    <nav class="p-4 space-y-2">

      <button
        v-for="link in links"
        :key="link.name"
        @click="router.push(link.path)"
        class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition"
      >
        <!-- icon placeholder -->
        <span>•</span>

        <span v-if="open">{{ link.name }}</span>
      </button>

    </nav>

    <!-- USER/LOGOUT -->
     <div class="p-4 border-t border-border">

      <button @click="handleLogout" class="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-red-500 hover:bg-red-50 transition">

        <span class="text-lg">⎋</span>

        <span class="text-lg">
          Logout
        </span>

      </button>
     </div>

  </aside>
</template>