<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import PageHeader from '@/components/admin/PageHeader.vue'
import StatCard from '@/components/admin/StatCard.vue'
import EmptyState from '@/components/admin/EmptyState.vue'
import StatusBadge from '@/components/admin/StatusBadge.vue'
import DeleteModal from '@/components/admin/DeleteModal.vue'
import ViewModal from '@/components/admin/ViewModal.vue'
import { useInquiryStore } from '@/stores/inquiry'

import axios from 'axios'
import { API_BASE_URI } from '@/config/api'

const store = useInquiryStore()

// ========== Filters & Search ==========
const search = ref('')
const statusFilter = ref('') // empty = all

// ========== Sorting ==========
type SortField = 'client_name' | 'service' | 'status' | 'created_at'
const sortField = ref<SortField>('created_at')
const sortOrder = ref<'asc' | 'desc'>('desc')

// ========== Pagination ==========
const currentPage = ref(1)
const itemsPerPage = 10

// ========== Bulk Delete ==========
const selectedIds = ref<number[]>([])
const selectAll = ref(false)

// ========== Delete Modal ==========
const showDeleteModal = ref(false)
const inquiryToDelete = ref<number | null>(null)

// ========== View Modal ==========
const showViewModal = ref(false)
const selectedInquiry = ref<any>(null)

// ========== Loading ==========
const isLoading = computed(() => store.loading)

// ========== Data ==========
onMounted(() => {
  store.load()
})

// Reset page when filters/sort change
watch([search, statusFilter, sortField, sortOrder], () => {
  currentPage.value = 1
  selectAll.value = false
  selectedIds.value = []
})

// ---------- Filtering ----------
const filteredInquiries = computed(() => {
  let filtered = store.inquiries

  // Search filter (by client name)
  if (search.value.trim()) {
    const query = search.value.toLowerCase()
    filtered = filtered.filter((item: any) =>
      item.client_details?.name?.toLowerCase().includes(query)
    )
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter((item: any) => item.status === statusFilter.value)
  }

  return filtered
})

// ---------- Sorting ----------
const sortedInquiries = computed(() => {
  const filtered = filteredInquiries.value
  return [...filtered].sort((a: any, b: any) => {
    let aVal: any
    let bVal: any

    switch (sortField.value) {
      case 'client_name':
        aVal = a.client_details?.name || ''
        bVal = b.client_details?.name || ''
        break
      case 'service':
        aVal = a.service || ''
        bVal = b.service || ''
        break
      case 'status':
        aVal = a.status || ''
        bVal = b.status || ''
        break
      case 'created_at':
        aVal = new Date(a.created_at).getTime()
        bVal = new Date(b.created_at).getTime()
        break
      default:
        aVal = a[sortField.value]
        bVal = b[sortField.value]
    }

    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

// ---------- Pagination ----------
const paginatedInquiries = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedInquiries.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedInquiries.value.length / itemsPerPage))

// ---------- Stats ----------
const totalInquiries = computed(() => store.inquiries.length)
const pendingInquiries = computed(() => store.inquiries.filter((i: any) => i.status === 'new').length)
const completedInquiries = computed(() => store.inquiries.filter((i: any) => i.status === 'completed').length)

// ---------- Bulk Select Logic ----------
watch(selectAll, (newVal) => {
  if (newVal) {
    selectedIds.value = paginatedInquiries.value.map((c: any) => c.id)
  } else {
    selectedIds.value = []
  }
})

watch([currentPage, paginatedInquiries], () => {
  selectAll.value = false
  selectedIds.value = selectedIds.value.filter(id =>
    store.inquiries.some((i: any) => i.id === id)
  )
})

const toggleSelect = (id: number) => {
  if (selectedIds.value.includes(id)) {
    selectedIds.value = selectedIds.value.filter(i => i !== id)
  } else {
    selectedIds.value.push(id)
  }
  const allCurrentSelected = paginatedInquiries.value.every((i: any) => selectedIds.value.includes(i.id))
  selectAll.value = allCurrentSelected && paginatedInquiries.value.length > 0
}

// ---------- Actions ----------
const confirmDelete = (id: number) => {
  inquiryToDelete.value = id
  showDeleteModal.value = true
}

const deleteConfirmed = async () => {
  if (!inquiryToDelete.value) return
  await store.remove(inquiryToDelete.value)
  showDeleteModal.value = false
  inquiryToDelete.value = null
  selectedIds.value = selectedIds.value.filter(id => id !== inquiryToDelete.value)
}

const bulkDelete = async () => {
  if (selectedIds.value.length === 0) return
  const confirmed = confirm(`Delete ${selectedIds.value.length} inquiry(ies)?`)
  if (!confirmed) return
  for (const id of selectedIds.value) {
    await store.remove(id)
  }
  selectedIds.value = []
  selectAll.value = false
}

const changeStatus = async (id: number, event: Event) => {
  const target = event.target as HTMLSelectElement
  await store.updateStatus(id, target.value)
  // No need to reset page, status filter might affect current page – but we keep page as is
}

const openViewModal = (inquiry: any) => {
  selectedInquiry.value = inquiry
  showViewModal.value = true
}

// ---------- Export CSV ----------
const exportToCSV = () => {
  const headers = ['Client Name', 'Email', 'Service', 'Budget', 'Status', 'Message', 'Date']
  const rows = sortedInquiries.value.map((i: any) => [
    i.client_details?.name || '',
    i.client_details?.email || '',
    i.service || '',
    i.budget || '',
    i.status || '',
    i.message || '',
    new Date(i.created_at).toLocaleDateString()
  ])
  const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.setAttribute('download', 'inquiries.csv')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// ---------- Sorting Helper ----------
const toggleSort = (field: SortField) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
}

// Quotation data for the current inquiry
const quotation = ref<any>(null)
const showQuotationForm = ref(false)
const savingQuotation = ref(false)

// Form for new quotation
const quotationForm = ref({
  valid_until: '',
  description: '',
  line_items: [] as { service: string; price: number }[]
})

// Helper to parse services from the inquiry
const getServiceArray = (): string[] => {
    if (!selectedInquiry.value?.service) return []
    return selectedInquiry.value.service.split(',').map((s: string) => s.trim())
}

// Auto‑generate a unique quotation number (frontend version)
const generateQuotationNumber = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  return `Q-${year}${month}-${random}`
}

// Fetch existing quotation for this inquiry (if any)
const fetchQuotation = async (inquiryId: number) => {
  try {
    const res = await axios.get(`${API_BASE_URI}/quotation/?inquiry=${inquiryId}`)
    quotation.value = res.data.length ? res.data[0] : null
  } catch (error) {
    console.error('Failed to fetch quotation', error)
  }
}

// Create a new quotation
const createQuotation = async () => {
  if (!selectedInquiry.value) return
  savingQuotation.value = true
  try {
    const payload = {
      inquiry: selectedInquiry.value.id,
      description: quotationForm.value.description,
      valid_until: quotationForm.value.valid_until,
      line_items: quotationForm.value.line_items,
      status: 'pending'
    }
    const res = await axios.post(`${API_BASE_URI}/quotation/`, payload)
    quotation.value = res.data
    showQuotationForm.value = false
    quotationForm.value = { line_items: [], description: '', valid_until: '' }
  } catch (err: any) {
    console.error('Quotation creation failed', err)
    if (err.response) alert(`Error: ${JSON.stringify(err.response.data)}`)
  } finally {
    savingQuotation.value = false
  }
}

// Modify openViewModal to also fetch any existing quotation
const originalOpenViewModal = openViewModal // rename if needed
const openViewModalWithQuotation = async (inquiry: any) => {
  // Reset for the new inquiry
  quotation.value = null
  showQuotationForm.value = false
  selectedInquiry.value = inquiry
  showViewModal.value = true
  await fetchQuotation(inquiry.id)
}

// ComputedTotal
const computedTotal = computed(() => {
    return quotationForm.value.line_items.reduce((sum, item) => sum + (item.price || 0), 0)
})

// prepareQuotationForm
const prepareQuotationForm = () => {
    const services = getServiceArray()

    // Default valid until = 3o days from today
    const defaultDate = new Date()
    defaultDate.setDate(defaultDate.getDate() + 30)
    const year = defaultDate.getFullYear()
    const month = String(defaultDate.getMonth() + 1).padStart(2, '0')
    const day = String(defaultDate.getDate()).padStart(2, '0')
    const defaultValidUntil = `${year}-${month}-${day}`

    quotationForm.value = {
        valid_until: defaultValidUntil,
        description: '',
        line_items: services.map((service: string) => ({ service, price: 0 }))
    }
    showQuotationForm.value = true
}

</script>

<template>
  <div class="space-y-8">
    <!-- Header -->
    <PageHeader title="Inquiries" subtitle="Manage client leads and project requests." />

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard title="Total Inquiries" :value="totalInquiries" icon="📨" />
      <StatCard title="Pending" :value="pendingInquiries" icon="⏳" />
      <StatCard title="Completed" :value="completedInquiries" icon="✅" />
    </div>

    <!-- Search + Filter + Export + Bulk Delete Bar -->
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div class="flex flex-1 gap-3 flex-wrap">
        <div class="relative flex-1 min-w-[200px]">
          <input
            v-model="search"
            type="text"
            placeholder="Search by client name..."
            class="w-full px-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>
        <select
          v-model="statusFilter"
          class="px-4 py-3 border rounded-2xl bg-white outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="">All Statuses</option>
          <option value="new">New</option>
          <option value="quoted">Quoted</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
        <button
          @click="exportToCSV"
          class="px-5 py-3 bg-green-50 text-green-700 rounded-2xl hover:bg-green-100 transition"
        >
          📎 Export CSV
        </button>
        <button
          v-if="selectedIds.length"
          @click="bulkDelete"
          class="px-5 py-3 bg-red-50 text-red-600 rounded-2xl hover:bg-red-100 transition"
        >
          🗑 Delete Selected ({{ selectedIds.length }})
        </button>
      </div>
    </div>

    <!-- Loading State (Skeleton) -->
    <div v-if="isLoading" class="space-y-4">
      <div class="bg-white rounded-3xl border p-4 shadow-sm">
        <div class="h-12 bg-gray-100 rounded-2xl animate-pulse"></div>
      </div>
      <div class="bg-white rounded-3xl border overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b">
              <tr class="text-left text-sm text-gray-500">
                <th class="px-6 py-4 w-10"><div class="h-4 bg-gray-200 rounded w-5"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-16"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-16"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-16"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-16"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-16"></div></th>
                <th class="px-6 py-4 text-right"><div class="h-4 bg-gray-200 rounded w-12 ml-auto"></div></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 5" :key="n" class="border-b">
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-5"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-32"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-28"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-24"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-20"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-24"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-16 ml-auto"></div></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Table (when data exists) -->
    <div
      v-else-if="sortedInquiries.length"
      class="bg-white rounded-3xl border shadow-sm overflow-hidden"
    >
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr class="text-left text-sm text-gray-500">
              <th class="px-6 py-4 w-10">
                <input type="checkbox" v-model="selectAll" />
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('client_name')">
                Client
                <span v-if="sortField === 'client_name'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('service')">
                Service
                <span v-if="sortField === 'service'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <!-- <th class="px-6 py-4">Budget</th> -->
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('status')">
                Status
                <span v-if="sortField === 'status'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('created_at')">
                Date
                <span v-if="sortField === 'created_at'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedInquiries"
              :key="item.id"
              class="border-b last:border-0 hover:bg-gray-50 transition"
            >
              <td class="px-6 py-5">
                <input type="checkbox" :checked="selectedIds.includes(item.id)" @change="toggleSelect(item.id)" />
              </td>
              <td class="px-6 py-5">
                <div>
                  <p class="font-semibold text-gray-800">{{ item.client_details?.name }}</p>
                  <p class="text-sm text-gray-500">{{ item.client_details?.email }}</p>
                </div>
              </td>
              <td class="px-6 py-5">{{ item.service }}</td>
              <!-- <td class="px-6 py-5">{{ item.budget || '—' }}</td> -->
              <td class="px-6 py-5">
                <div class="flex flex-col gap-2">
                  <StatusBadge :status="item.status" />
                  <select
                    :value="item.status"
                    @change="changeStatus(item.id, $event)"
                    class="px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    <option value="new">New</option>
                    <option value="quoted">Quoted</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>
              </td>
              <td class="px-6 py-5 text-sm text-gray-500">
                {{ new Date(item.created_at).toLocaleDateString() }}
              </td>
              <td class="px-6 py-5">
                <div class="flex items-center justify-end gap-2">
                  <button
                    @click="openViewModalWithQuotation(item)"
                    class="px-3 py-2 rounded-xl bg-blue-50 text-blue-600 hover:bg-blue-100 transition text-sm"
                  >
                    View
                  </button>
                  <button
                    @click="confirmDelete(item.id)"
                    class="px-3 py-2 rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition text-sm"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="px-6 py-4 border-t flex justify-between items-center flex-wrap gap-3">
        <div class="text-sm text-gray-500">
          Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, sortedInquiries.length) }} of {{ sortedInquiries.length }} inquiries
        </div>
        <div class="flex gap-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-4 py-2 rounded-xl border bg-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 transition"
          >
            ← Prev
          </button>
          <span class="px-4 py-2 text-sm text-gray-600">Page {{ currentPage }} of {{ totalPages || 1 }}</span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="px-4 py-2 rounded-xl border bg-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 transition"
          >
            Next →
          </button>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <EmptyState
      v-else
      title="No inquiries found"
      message="Try adjusting your search or filters, or wait for new client inquiries."
    />

    <!-- View Modal (reusable) -->
    <ViewModal :show="showViewModal" title="Inquiry Details" @close="showViewModal = false; quotation = null; showQuotationForm = false">
  <div class="space-y-6">
    <!-- Existing inquiry details (keep as is) -->
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
        <p class="text-sm text-gray-500">Budget</p>
        <p class="font-medium">{{ selectedInquiry?.budget || '—' }}</p>
      </div>
      <div>
        <p class="text-sm text-gray-500">Message</p>
        <p class="text-sm">{{ selectedInquiry?.message || '—' }}</p>
      </div>
      <div>
        <p class="text-sm text-gray-500">Status</p>
        <StatusBadge :status="selectedInquiry?.status" />
      </div>
    </div>

    <hr />

    <!-- Quotation Section -->
    <div>
      <div class="flex justify-between items-center mb-3">
        <h3 class="font-semibold text-lg">Quotation</h3>
        <button
          v-if="!quotation && !showQuotationForm"
          @click="prepareQuotationForm"
          class="px-3 py-1 bg-primary text-white rounded-xl text-sm"
        >
          + Create Quotation
        </button>
      </div>

      <!-- Show existing quotation -->
      <div v-if="quotation" class="bg-gray-50 rounded-2xl p-4 space-y-2">
        <div class="flex justify-between">
          <span class="font-mono text-sm">#{{ quotation.quotation_number }}</span>
          <span :class="{
            'bg-yellow-100 text-yellow-700': quotation.status === 'pending',
            'bg-green-100 text-green-700': quotation.status === 'approved',
            'bg-red-100 text-red-700': quotation.status === 'rejected'
          }" class="px-2 py-0.5 rounded-full text-xs">{{ quotation.status }}</span>
        </div>
        <div>
          <p class="text-xs text-gray-500">Amount (KSh)</p>
          <p class="text-xl font-bold">{{ parseFloat(quotation.amount).toLocaleString() }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500">Valid Until</p>
          <p>{{ new Date(quotation.valid_until).toLocaleDateString() }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500">Description</p>
          <p class="text-sm">{{ quotation.description }}</p>
        </div>
      </div>

      <!-- Create Quotation Form -->
      <div v-if="showQuotationForm" class="bg-white border rounded-2xl p-4 space-y-3">
        <!-- Dynamic line items -->
        <div class="space-y-2">
            <label class="block text-sm font-medium">Services & Prices</label>
            <div v-for="(item, idx) in quotationForm.line_items" :key="idx" class="flex gap-2 items-center">
            <span class="flex-1 text-sm">{{ item.service }}</span>
            <input
                v-model.number="item.price"
                type="number"
                step="0.01"
                placeholder="Price (KSh)"
                class="w-32 border rounded-xl px-3 py-2 text-sm"
            />
            </div>
            <!-- Optional: add a custom line item -->
            <button
            @click="quotationForm.line_items.push({ service: '', price: 0 })"
            class="text-xs text-primary underline mt-1"
            >
            + Add custom service
            </button>
        </div>

        <textarea
            v-model="quotationForm.description"
            rows="3"
            placeholder="Additional description (optional)"
            class="w-full border rounded-xl px-3 py-2 text-sm"
        ></textarea>

        <input
            v-model="quotationForm.valid_until"
            type="date"
            required
            class="w-full border rounded-xl px-3 py-2 text-sm"
        />

        <div class="flex justify-between items-center">
            <span class="font-semibold">Total: KSh {{ computedTotal }}</span>
            <div class="flex gap-2">
            <button
                @click="createQuotation"
                :disabled="savingQuotation"
                class="px-4 py-2 bg-primary text-white rounded-xl text-sm"
            >
                {{ savingQuotation ? 'Saving...' : 'Save Quotation' }}
            </button>
            <button
                @click="showQuotationForm = false"
                class="px-4 py-2 border rounded-xl text-sm"
            >
                Cancel
            </button>
            </div>
        </div>
        </div>
    </div>
  </div>
</ViewModal>
                                          
<!-- Delete Modal (single) -->
<DeleteModal
    :show="showDeleteModal"
    title="Delete Inquiry?"
    message="This inquiry will be permanently removed."
    @close="showDeleteModal = false"
    @confirm="deleteConfirmed"
/>
</div>

</template>