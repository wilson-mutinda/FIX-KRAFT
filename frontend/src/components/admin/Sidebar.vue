<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'

import {
  LayoutDashboard,
  Briefcase,
  Users,
  Receipt,
  Wallet,
  FolderKanban,
  Settings,
  Image,
  MessageSquare,
  LogOut
} from 'lucide-vue-next'
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { API_BASE_URI } from '@/config/api';

defineProps<{
  open: boolean
}>()

const router = useRouter()
const route = useRoute()

const auth = useAuthStore()

const links = [
  {
    name: 'Dashboard',
    path: '/admin',
    icon: LayoutDashboard
  },
  {
    name: 'Inquiries',
    path: '/admin/inquiries',
    icon: MessageSquare
  },
  {
    name: 'Clients',
    path: '/admin/clients',
    icon: Users
  },
  {
    name: 'Quotations',
    path: '/admin/quotations',
    icon: Receipt
  },
  {
    name: 'Payments',
    path: '/admin/payments',
    icon: Wallet
  },
  {
    name: 'Projects',
    path: '/admin/projects',
    icon: FolderKanban
  },
  {
    name: 'Services',
    path: '/admin/services',
    icon: Briefcase
  },
  {
    name: 'Media',
    path: '/admin/media',
    icon: Image
  },
  {
    name: 'Settings',
    path: '/admin/settings',
    icon: Settings
  }
]

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}

const counts = ref({
  inquiries_new: 0,
  clients_total: 0,
  quotations_pending: 0,
  payments_total: 0
})

onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE_URI}/counts/`)
    counts.value = res.data
  } catch (error) {
    console.error('Failed to fetch counts', error)
  }
})

</script>

<template>
  <aside
    :class="[
      'bg-white border-r border-gray-100 h-full transition-all duration-300 flex flex-col',
      open ? 'w-64' : 'w-20'
    ]"
  >

    <!-- LOGO -->
    <div class="h-16 flex items-center justify-center border-b border-gray-100">
      <span class="font-bold text-primary text-lg">
        {{ open ? 'FixKraft' : 'FK' }}
      </span>
    </div>

    <!-- LINKS -->
    <nav class="flex-1 p-4 space-y-2 overflow-y-auto">

      <button
        v-for="link in links"
        :key="link.name"
        @click="router.push(link.path)"
        :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-200',
          route.path === link.path
            ? 'bg-primary text-white shadow-lg'
            : 'text-gray-600 hover:bg-gray-100'
        ]"
      >

        <component :is="link.icon" class="w-5 h-5 shrink-0" />

        <span
          v-if="open"
          class="text-sm font-medium"
        >
          {{ link.name }}
        </span>

        <!-- Badge for inquiries -->
         <span v-if="link.name === 'Inquiries' && counts.inquiries_new > 0" class="bg-green-500 text-white text-xs rounded-full px-2 py-0.5">
          {{ counts.inquiries_new }}
         </span>
         <!-- Similar for quotations -->
          <span v-if="link.name === 'Quotations' && counts.quotations_pending > 0" class="bg-yellow-500 text-white text-sm rounded-full px-2 py-0.5">
            {{ counts.quotations_pending }}
          </span>

      </button>

    </nav>

    <!-- LOGOUT -->
    <div class="p-4 border-t border-gray-100">

      <button
        @click="handleLogout"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-red-500 hover:bg-red-50 transition"
      >

        <LogOut class="w-5 h-5" />

        <span
          v-if="open"
          class="font-medium"
        >
          Logout
        </span>

      </button>

    </div>

  </aside>
</template>
