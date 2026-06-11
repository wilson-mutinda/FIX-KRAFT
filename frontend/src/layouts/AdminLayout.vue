<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from '@/components/admin/Sidebar.vue'
import Topbar from '@/components/admin/Topbar.vue'
import ViewModal from '@/components/admin/ViewModal.vue'
import StatusBadge from '@/components/admin/StatusBadge.vue'
import { useInquiryStore } from '@/stores/inquiry'
import axios from 'axios'
import { API_BASE_URI } from '@/config/api'
import { useCountsStore } from '@/stores/counts'

const sidebarOpen = ref(true)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// Define the shape of an inquiry
interface Inquiry {
  id: number;
  client_details?: { name: string; email: string };
  service: string;
  message: string;
  status: string;
  created_at: string;
}

const selectedInquiry = ref<Inquiry | null>(null)
const showInquiryModal = ref(false)

const countsStore = useCountsStore()

const handleViewInquiry = async (id: number) => {
  const store = useInquiryStore()
  const inquiry = store.inquiries.find((i: any) => i.id === id)
  if (inquiry) {
    selectedInquiry.value = inquiry as Inquiry
    showInquiryModal.value = true

    // Mark as read
    try {
      await axios.patch(`${API_BASE_URI}/inquiries/${id}/mark_read/`)
      countsStore.fetchCounts()
      // Decrease unread count on topbar
    } catch (error) {
      console.error('Failed to mark as read', error)
    }
  }
}

</script>

<template>
  <div class="flex h-screen bg-gray-100">
    <!-- SIDEBAR -->
    <Sidebar :open="sidebarOpen" />

    <!-- MAIN CONTENT -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- TOPBAR (only once) -->
      <Topbar @toggle-sidebar="toggleSidebar" @view-inquiry="handleViewInquiry" />

      <!-- MAIN -->
      <main class="flex-1 overflow-y-auto p-6">
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </main>
    </div>
  </div>

  <!-- View Modal -->
  <ViewModal :show="showInquiryModal" title="Inquiry Details" @close="showInquiryModal = false">
    <div class="space-y-3">
      <div>
        <p class="text-sm text-gray-500">Client</p>
        <p class="font-medium">{{ selectedInquiry?.client_details?.name || '—' }}</p>
        <p class="text-sm text-gray-500">{{ selectedInquiry?.client_details?.email || '—' }}</p>
      </div>
      <div>
        <p class="text-sm text-gray-500">Service</p>
        <p class="font-medium">{{ selectedInquiry?.service || '—' }}</p>
      </div>
      <div>
        <p class="text-sm text-gray-500">Message</p>
        <p class="text-sm">{{ selectedInquiry?.message || '—' }}</p>
      </div>
      <div>
        <p class="text-sm text-gray-500">Status</p>
        <StatusBadge :status="selectedInquiry?.status || 'new'" />
      </div>
      <div>
        <p class="text-sm text-gray-500">Submitted</p>
        <p class="font-medium">{{ selectedInquiry?.created_at ? new Date(selectedInquiry.created_at).toLocaleDateString() : '—' }}</p>
      </div>
    </div>
  </ViewModal>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>