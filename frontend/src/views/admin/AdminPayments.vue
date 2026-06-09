<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import PageHeader from '@/components/admin/PageHeader.vue'
import StatCard from '@/components/admin/StatCard.vue'
import EmptyState from '@/components/admin/EmptyState.vue'
import DeleteModal from '@/components/admin/DeleteModal.vue'
import ViewModal from '@/components/admin/ViewModal.vue'
import { usePaymentStore } from '@/stores/payment'

const store = usePaymentStore()

// ========== Filters & Search ==========
const search = ref('')
const methodFilter = ref('') // '', 'Cash', 'M-Pesa', 'Card', etc.

// ========== Sorting ==========
type SortField = 'project_name' | 'amount' | 'payment_method' | 'created_at'
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
const paymentToDelete = ref<number | null>(null)

// ========== View Modal ==========
const showViewModal = ref(false)
const selectedPayment = ref<any>(null)

// ========== Loading ==========
const isLoading = computed(() => store.loading)

// ========== Data ==========
onMounted(() => {
  store.load()
})

watch([search, methodFilter, sortField, sortOrder], () => {
  currentPage.value = 1
  selectAll.value = false
  selectedIds.value = []
})

// ---------- Filtering ----------
const filteredPayments = computed(() => {
  let filtered = store.payments

  // Search: project title or transaction ID
  if (search.value.trim()) {
    const query = search.value.toLowerCase()
    filtered = filtered.filter(p => {
      const projectTitle = p.project_details?.title?.toString() || ''
      const transactionId = p.transaction_id?.toString() || ''
      return projectTitle.toLowerCase().includes(query) ||
             transactionId.toLowerCase().includes(query)
    })
  }

  // Payment method filter
  if (methodFilter.value) {
    filtered = filtered.filter(p => p.payment_method === methodFilter.value)
  }

  return filtered
})

// ---------- Sorting ----------
const sortedPayments = computed(() => {
  const filtered = filteredPayments.value
  return [...filtered].sort((a, b) => {
    let aVal: any, bVal: any
    switch (sortField.value) {
      case 'project_name':
        aVal = a.project_details?.title || ''
        bVal = b.project_details?.title || ''
        break
      case 'amount':
        aVal = parseFloat(a.amount)
        bVal = parseFloat(b.amount)
        break
      case 'payment_method':
        aVal = a.payment_method
        bVal = b.payment_method
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
const paginatedPayments = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedPayments.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedPayments.value.length / itemsPerPage))

// ---------- Stats ----------
const totalPayments = computed(() => store.payments.length)
const totalAmount = computed(() => {
  return store.payments.reduce((sum, p) => sum + parseFloat(p.amount), 0)
})
const uniqueTransactions = computed(() => store.payments.length) // or count distinct transaction_id? Keep simple.

// ---------- Bulk Select Logic ----------
watch(selectAll, (newVal) => {
  if (newVal) {
    selectedIds.value = paginatedPayments.value.map(p => p.id)
  } else {
    selectedIds.value = []
  }
})

watch([currentPage, paginatedPayments], () => {
  selectAll.value = false
  selectedIds.value = selectedIds.value.filter(id =>
    store.payments.some(p => p.id === id)
  )
})

const toggleSelect = (id: number) => {
  if (selectedIds.value.includes(id)) {
    selectedIds.value = selectedIds.value.filter(i => i !== id)
  } else {
    selectedIds.value.push(id)
  }
  const allCurrentSelected = paginatedPayments.value.every(p => selectedIds.value.includes(p.id))
  selectAll.value = allCurrentSelected && paginatedPayments.value.length > 0
}

// ---------- Actions ----------
const confirmDelete = (id: number) => {
  paymentToDelete.value = id
  showDeleteModal.value = true
}

const deleteConfirmed = async () => {
  if (!paymentToDelete.value) return
  await store.remove(paymentToDelete.value)
  showDeleteModal.value = false
  paymentToDelete.value = null
  selectedIds.value = selectedIds.value.filter(id => id !== paymentToDelete.value)
}

const bulkDelete = async () => {
  if (selectedIds.value.length === 0) return
  const confirmed = confirm(`Delete ${selectedIds.value.length} payment(s)?`)
  if (!confirmed) return
  for (const id of selectedIds.value) {
    await store.remove(id)
  }
  selectedIds.value = []
  selectAll.value = false
}

const openViewModal = (payment: any) => {
  selectedPayment.value = payment
  showViewModal.value = true
}

// ---------- Export CSV ----------
const exportToCSV = () => {
  const headers = ['Project', 'Amount', 'Payment Method', 'Transaction ID', 'Date']
  const rows = sortedPayments.value.map(p => [
    p.project_details?.title || '',
    p.amount,
    p.payment_method,
    p.transaction_id,
    new Date(p.created_at).toLocaleDateString()
  ])
  const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.setAttribute('download', 'payments.csv')
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
    <PageHeader title="Payments" subtitle="Track all financial transactions from projects." />

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard title="Total Payments" :value="totalPayments" icon="💰" />
      <StatCard title="Total Amount" :value="`KSh ${totalAmount.toLocaleString()}`" icon="💵" />
      <StatCard title="Transactions" :value="uniqueTransactions" icon="🧾" />
    </div>

    <!-- Search + Filter + Export + Bulk Delete Bar -->
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div class="flex flex-1 gap-3 flex-wrap">
        <div class="relative flex-1 min-w-[200px]">
          <input
            v-model="search"
            type="text"
            placeholder="Search by project or transaction ID..."
            class="w-full px-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>
        <select
          v-model="methodFilter"
          class="px-4 py-3 border rounded-2xl bg-white outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="">All Payment Methods</option>
          <option value="Cash">Cash</option>
          <option value="M-Pesa">M-Pesa</option>
          <option value="Bank Transfer">Bank Transfer</option>
          <option value="Card">Card</option>
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
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-20"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-32"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></th>
                <th class="px-6 py-4 text-right"><div class="h-4 bg-gray-200 rounded w-12 ml-auto"></div></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 5" :key="n" class="border-b">
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-5"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-32"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-24"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-28"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-36"></div></td>
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
      v-else-if="sortedPayments.length"
      class="bg-white rounded-3xl border shadow-sm overflow-hidden"
    >
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr class="text-left text-sm text-gray-500">
              <th class="px-6 py-4 w-10">
                <input type="checkbox" v-model="selectAll" />
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('project_name')">
                Project
                <span v-if="sortField === 'project_name'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('amount')">
                Amount (KSh)
                <span v-if="sortField === 'amount'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('payment_method')">
                Method
                <span v-if="sortField === 'payment_method'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4">Transaction ID</th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('created_at')">
                Date
                <span v-if="sortField === 'created_at'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedPayments"
              :key="item.id"
              class="border-b last:border-0 hover:bg-gray-50 transition"
            >
              <td class="px-6 py-5">
                <input type="checkbox" :checked="selectedIds.includes(item.id)" @change="toggleSelect(item.id)" />
              </td>
              <td class="px-6 py-5 font-medium text-gray-800">
                {{ item.project_details?.title || '—' }}
              </td>
              <td class="px-6 py-5">
                {{ parseFloat(item.amount).toLocaleString() }}
              </td>
              <td class="px-6 py-5">
                <span class="px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-700">
                  {{ item.payment_method }}
                </span>
              </td>
              <td class="px-6 py-5 font-mono text-sm">
                {{ item.transaction_id }}
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
          Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, sortedPayments.length) }} of {{ sortedPayments.length }} payments
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
      title="No payments found"
      message="Try adjusting your search or filters, or add a new payment from a project."
    />

    <!-- View Modal (reusable) -->
    <ViewModal :show="showViewModal" title="Payment Details" @close="showViewModal = false">
      <div class="space-y-3">
        <div>
          <p class="text-sm text-gray-500">Project</p>
          <p class="font-medium">{{ selectedPayment?.project_details?.title || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Amount</p>
          <p class="font-medium">KSh {{ selectedPayment?.amount ? parseFloat(selectedPayment.amount).toLocaleString() : '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Payment Method</p>
          <p class="font-medium">{{ selectedPayment?.payment_method || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Transaction ID</p>
          <p class="font-mono text-sm">{{ selectedPayment?.transaction_id || '—' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500">Date</p>
          <p class="font-medium">{{ selectedPayment?.created_at ? new Date(selectedPayment.created_at).toLocaleDateString() : '—' }}</p>
        </div>
      </div>
    </ViewModal>

    <!-- Delete Modal (single) -->
    <DeleteModal
      :show="showDeleteModal"
      title="Delete Payment?"
      message="This payment record will be permanently removed."
      @close="showDeleteModal = false"
      @confirm="deleteConfirmed"
    />
  </div>
</template>