<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import PageHeader from '@/components/admin/PageHeader.vue'
import StatCard from '@/components/admin/StatCard.vue'
import EmptyState from '@/components/admin/EmptyState.vue'
import DeleteModal from '@/components/admin/DeleteModal.vue'
import ViewModal from '@/components/admin/ViewModal.vue'
import StatusBadge from '@/components/admin/StatusBadge.vue'
import { useClientStore } from '@/stores/client'

const store = useClientStore()

// ========== Filters & Search ==========
const search = ref('')
const statusFilter = ref('') // empty = all

// ========== Sorting ==========
type SortField = 'name' | 'company' | 'created_at'
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
const clientToDelete = ref<number | null>(null)

// ========== View Modal ==========
const showViewModal = ref(false)
const selectedClient = ref<any>(null)

// ========== Loading ==========
const isLoading = computed(() => store.loading)

// ========== Data ==========
onMounted(() => {
  store.load()
})

// Watch for filter changes -> reset to page 1
watch([search, statusFilter, sortField, sortOrder], () => {
  currentPage.value = 1
  selectAll.value = false
  selectedIds.value = []
})

// ---------- Filtering ----------
const filteredClients = computed(() => {
  let filtered = store.clients

  // Search filter
  if (search.value.trim()) {
    const query = search.value.toLowerCase()
    filtered = filtered.filter(
      (item: any) =>
        item.name?.toLowerCase().includes(query) ||
        item.email?.toLowerCase().includes(query) ||
        item.company?.toLowerCase().includes(query)
    )
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter((item: any) => item.status === statusFilter.value)
  }

  return filtered
})

// ---------- Sorting ----------
const sortedClients = computed(() => {
  const filtered = filteredClients.value
  return [...filtered].sort((a: any, b: any) => {
    let aVal = a[sortField.value]
    let bVal = b[sortField.value]

    if (sortField.value === 'created_at') {
      aVal = new Date(aVal).getTime()
      bVal = new Date(bVal).getTime()
    }

    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

// ---------- Pagination ----------
const paginatedClients = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedClients.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedClients.value.length / itemsPerPage))

// ---------- Stats ----------
const totalClients = computed(() => store.clients.length)
const companyClients = computed(() => store.clients.filter((item: any) => item.company).length)

// ---------- Bulk Select Logic ----------
watch(selectAll, (newVal) => {
  if (newVal) {
    selectedIds.value = paginatedClients.value.map((c: any) => c.id)
  } else {
    selectedIds.value = []
  }
})

// When pagination changes, reset selectAll checkbox
watch([currentPage, paginatedClients], () => {
  selectAll.value = false
  // Keep selectedIds only for items still in the list (optional)
  selectedIds.value = selectedIds.value.filter(id =>
    store.clients.some((c: any) => c.id === id)
  )
})

// Toggle individual checkbox
const toggleSelect = (id: number) => {
  if (selectedIds.value.includes(id)) {
    selectedIds.value = selectedIds.value.filter(i => i !== id)
  } else {
    selectedIds.value.push(id)
  }
  // Update selectAll based on current page
  const allCurrentSelected = paginatedClients.value.every((c: any) => selectedIds.value.includes(c.id))
  selectAll.value = allCurrentSelected && paginatedClients.value.length > 0
}

// ---------- Actions ----------
const confirmDelete = (id: number) => {
  clientToDelete.value = id
  showDeleteModal.value = true
}

const deleteConfirmed = async () => {
  if (!clientToDelete.value) return
  await store.remove(clientToDelete.value)
  showDeleteModal.value = false
  clientToDelete.value = null
  // Remove from selectedIds if present
  selectedIds.value = selectedIds.value.filter(id => id !== clientToDelete.value)
}

const bulkDelete = async () => {
  if (selectedIds.value.length === 0) return
  const confirmed = confirm(`Delete ${selectedIds.value.length} client(s)?`)
  if (!confirmed) return
  // Sequential deletion (could be optimised with a bulk endpoint)
  for (const id of selectedIds.value) {
    await store.remove(id)
  }
  selectedIds.value = []
  selectAll.value = false
}

const openViewModal = (client: any) => {
  selectedClient.value = client
  showViewModal.value = true
}

// ---------- Export CSV ----------
const exportToCSV = () => {
  const headers = ['Name', 'Email', 'Phone', 'Company', 'Status', 'Joined Date']
  const rows = sortedClients.value.map((c: any) => [
    c.name,
    c.email,
    c.phone || '',
    c.company || '',
    c.status || 'lead',
    new Date(c.created_at).toLocaleDateString()
  ])
  const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.setAttribute('download', 'clients.csv')
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
</script>

<template>
  <div class="space-y-8">
    <!-- Header -->
    <PageHeader title="Clients" subtitle="Manage client relationships and business records." />

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <StatCard title="Total Clients" :value="totalClients" icon="👥" />
      <StatCard title="Companies" :value="companyClients" icon="🏢" />
    </div>

    <!-- Search + Filter + Export + Bulk Delete Bar -->
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div class="flex flex-1 gap-3 flex-wrap">
        <div class="relative flex-1 min-w-[200px]">
          <input
            v-model="search"
            type="text"
            placeholder="Search by name, email or company..."
            class="w-full px-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>
        <select
          v-model="statusFilter"
          class="px-4 py-3 border rounded-2xl bg-white outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="lead">Lead</option>
          <option value="churned">Churned</option>
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

    <!-- Loading State -->
    <div v-if="isLoading" class="space-y-4">
      <div class="bg-white rounded-3xl border p-4 shadow-sm">
        <div class="h-12 bg-gray-100 rounded-2xl animate-pulse"></div>
      </div>
      <div class="bg-white rounded-3xl border overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b">
              <tr>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-5"></div></th>
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
      v-else-if="sortedClients.length"
      class="bg-white rounded-3xl border shadow-sm overflow-hidden"
    >
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr class="text-left text-sm text-gray-500">
              <th class="px-6 py-4 w-10">
                <input type="checkbox" v-model="selectAll" />
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('name')">
                Client
                <span v-if="sortField === 'name'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4">Phone</th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('company')">
                Company
                <span v-if="sortField === 'company'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4">Status</th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('created_at')">
                Joined
                <span v-if="sortField === 'created_at'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedClients"
              :key="item.id"
              class="border-b last:border-0 hover:bg-gray-50 transition"
            >
              <td class="px-6 py-5">
                <input type="checkbox" :checked="selectedIds.includes(item.id)" @change="toggleSelect(item.id)" />
              </td>
              <td class="px-6 py-5">
                <div>
                  <p class="font-semibold text-gray-800">{{ item.name }}</p>
                  <p class="text-sm text-gray-500">{{ item.email }}</p>
                </div>
              </td>
              <td class="px-6 py-5">{{ item.phone || '—' }}</td>
              <td class="px-6 py-5">{{ item.company || '—' }}</td>
              <td class="px-6 py-5">
                <StatusBadge :status="item.status" />
              </td>
              <td class="px-6 py-5 text-sm text-gray-500">
                {{ new Date(item.created_at).toLocaleDateString() }}
              </td>
              <td class="px-6 py-5">
                <div class="flex items-center justify-end gap-2">
                  <button
                    @click="openViewModal(item)"
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
          Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, sortedClients.length) }} of {{ sortedClients.length }} clients
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

    <!-- Empty state (no data after filtering) -->
    <EmptyState
      v-else
      title="No clients found"
      message="Try adjusting your search or filters, or add a new client."
    />

    <!-- View Modal -->
    <ViewModal :show="showViewModal" title="Client Details" @close="showViewModal = false">
      <div class="space-y-3">
        <div>
          <p class="text-sm text-gray-500">Full Name</p>
          <p class="font-medium">{{ selectedClient?.name || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Email</p>
          <p class="font-medium">{{ selectedClient?.email || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Phone</p>
          <p class="font-medium">{{ selectedClient?.phone || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Company</p>
          <p class="font-medium">{{ selectedClient?.company || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Status</p>
          <StatusBadge :status="selectedClient?.status || 'lead'" />
        </div>
        <div>
          <p class="text-sm text-gray-500">Joined</p>
          <p class="font-medium">{{ selectedClient?.created_at ? new Date(selectedClient.created_at).toLocaleDateString() : '—' }}</p>
        </div>
      </div>
    </ViewModal>

    <!-- Delete Modal (single) -->
    <DeleteModal
      :show="showDeleteModal"
      title="Delete Client?"
      message="This client will be permanently removed."
      @close="showDeleteModal = false"
      @confirm="deleteConfirmed"
    />
  </div>
</template>