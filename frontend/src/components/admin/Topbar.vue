<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const emit = defineEmits(['toggle-sidebar'])
const router = useRouter()

const unreadCount = ref(0)
const showDropdown = ref(false)

// const recentInquiries = ref([])
interface Inquiry {
  id: number;
  client_details?: { name: string };
  service: string;
  status: string;
  created_at: string;
}

const recentInquiries = ref<Inquiry[]>([])

const fetchUnreadCount = async () => {
  try {
    const res = await axios.get('/api/inquiries/unread_count/')
    unreadCount.value = res.data.count
  } catch (error) {
    console.error('Failed to fetch unread count', error)
  }
}

const fetchRecentInquiries = async () => {
  try {
    const res = await axios.get('/api/inquiries/?ordering=-created_at&limit=5')
    recentInquiries.value = res.data
  } catch (error) {
    console.error('Failed to fetch recent inquiries', error)
  }
}

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    fetchRecentInquiries()
  }
}

const goToInquiry = (id: number) => {
  showDropdown.value = false
  router.push(`/admin/inquiries/${id}`)
}

let interval: number
onMounted(() => {
  fetchUnreadCount()
  interval = setInterval(fetchUnreadCount, 30000) // poll every 30s
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <header class="h-16 bg-white dark:bg-gray-900 border-b flex items-center justify-between px-6">
    <div class="flex items-center gap-4">
      <button @click="emit('toggle-sidebar')" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
        ☰
      </button>
      <h1 class="font-semibold text-gray-700 dark:text-gray-200">Admin Panel</h1>
    </div>

    <div class="flex items-center gap-4 relative">
      <!-- Bell with badge -->
      <button @click="toggleDropdown" class="relative p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
        <span class="text-xl">🔔</span>
        <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
          {{ unreadCount > 9 ? '9+' : unreadCount }}
        </span>
      </button>

      <!-- Dropdown -->
      <div v-if="showDropdown" class="absolute right-0 top-12 w-80 bg-white dark:bg-gray-800 border rounded-xl shadow-lg z-50">
        <div class="p-3 border-b font-semibold">Recent Inquiries</div>
        <div class="max-h-96 overflow-y-auto">
          <div v-for="inq in recentInquiries" :key="inq.id" @click="goToInquiry(inq.id)" class="p-3 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer border-b">
            <p class="text-sm font-medium">{{ inq.client_details?.name }}</p>
            <p class="text-xs text-gray-500">{{ inq.service }} – {{ inq.status }}</p>
            <p class="text-xs text-gray-400">{{ new Date(inq.created_at).toLocaleString() }}</p>
          </div>
          <div v-if="recentInquiries.length === 0" class="p-4 text-center text-gray-500">No inquiries yet</div>
        </div>
      </div>

      <!-- User avatar -->
      <div class="h-8 w-8 bg-gray-300 dark:bg-gray-600 rounded-full"></div>
    </div>
  </header>
</template>