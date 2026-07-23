<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import PageHeader from '@/components/admin/PageHeader.vue'
import StatCard from '@/components/admin/StatCard.vue'
import EmptyState from '@/components/admin/EmptyState.vue'
import DeleteModal from '@/components/admin/DeleteModal.vue'
import ViewModal from '@/components/admin/ViewModal.vue'
import { useQuotationStore } from '@/stores/quotation'
import EditQuotationModal from './EditQuotationModal.vue'
import html2pdf from 'html2pdf.js'
import axios from 'axios'
import { API_BASE_URI } from '@/config/api.ts'

const store = useQuotationStore()

// ========== Filters & Search ==========
const search = ref('')
const statusFilter = ref('') // pending, approved, rejected

// ========== Sorting ==========
type SortField = 'quotation_number' | 'amount' | 'status' | 'valid_until' | 'created_at'
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
const quotationToDelete = ref<number | null>(null)

// ========== View Modal ==========
const showViewModal = ref(false)
const selectedQuotation = ref<any>(null)

// ========== Edit Modal ==========
const showEditModal = ref(false)
const quotationToEdit = ref<any>(null)

// ========== Loading ==========
const isLoading = computed(() => store.loading)

// ========== Data ==========
onMounted(() => {
  store.load()
})

watch([search, statusFilter, sortField, sortOrder], () => {
  currentPage.value = 1
  selectAll.value = false
  selectedIds.value = []
})

// ---------- Filtering ----------
const filteredQuotations = computed(() => {
  let filtered = store.quotations

  if (search.value.trim()) {
    const query = search.value.toLowerCase()
    filtered = filtered.filter(q => {
      const clientName = q.inquiry_details?.client_details?.name?.toString() || ''
      const quotationNum = q.quotation_number?.toString() || ''
      return clientName.toLowerCase().includes(query) ||
             quotationNum.toLowerCase().includes(query)
    })
  }

  if (statusFilter.value) {
    filtered = filtered.filter(q => q.status === statusFilter.value)
  }

  return filtered
})

// ---------- Sorting ----------
const sortedQuotations = computed(() => {
  const filtered = filteredQuotations.value
  return [...filtered].sort((a, b) => {
    let aVal: any, bVal: any
    switch (sortField.value) {
      case 'quotation_number':
        aVal = a.quotation_number
        bVal = b.quotation_number
        break
      case 'amount':
        aVal = parseFloat(a.amount)
        bVal = parseFloat(b.amount)
        break
      case 'status':
        aVal = a.status
        bVal = b.status
        break
      case 'valid_until':
        aVal = new Date(a.valid_until).getTime()
        bVal = new Date(b.valid_until).getTime()
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
const paginatedQuotations = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedQuotations.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedQuotations.value.length / itemsPerPage))

// ---------- Stats ----------
const totalQuotations = computed(() => store.quotations.length)
const totalAmount = computed(() => {
  return store.quotations.reduce((sum, q) => sum + parseFloat(q.amount), 0)
})
const pendingCount = computed(() => store.quotations.filter(q => q.status === 'pending').length)

// ---------- Bulk Select ----------
watch(selectAll, (newVal) => {
  if (newVal) {
    selectedIds.value = paginatedQuotations.value.map(q => q.id)
  } else {
    selectedIds.value = []
  }
})

watch([currentPage, paginatedQuotations], () => {
  selectAll.value = false
  selectedIds.value = selectedIds.value.filter(id =>
    store.quotations.some(q => q.id === id)
  )
})

const toggleSelect = (id: number) => {
  if (selectedIds.value.includes(id)) {
    selectedIds.value = selectedIds.value.filter(i => i !== id)
  } else {
    selectedIds.value.push(id)
  }
  const allCurrentSelected = paginatedQuotations.value.every(q => selectedIds.value.includes(q.id))
  selectAll.value = allCurrentSelected && paginatedQuotations.value.length > 0
}

// ---------- Actions ----------
const confirmDelete = (id: number) => {
  quotationToDelete.value = id
  showDeleteModal.value = true
}

const deleteConfirmed = async () => {
  if (!quotationToDelete.value) return
  await store.remove(quotationToDelete.value)
  showDeleteModal.value = false
  quotationToDelete.value = null
  selectedIds.value = selectedIds.value.filter(id => id !== quotationToDelete.value)
}

const bulkDelete = async () => {
  if (selectedIds.value.length === 0) return
  const confirmed = confirm(`Delete ${selectedIds.value.length} quotation(s)?`)
  if (!confirmed) return
  for (const id of selectedIds.value) {
    await store.remove(id)
  }
  selectedIds.value = []
  selectAll.value = false
}

const openViewModal = (quotation: any) => {
  selectedQuotation.value = quotation
  showViewModal.value = true
}

const openEditModal = (quotation: any) => {
  quotationToEdit.value = quotation
  showEditModal.value = true
}

const handleEditSaved = async (updated: any) => {
  // The store update already handled in modal, but we can refresh if needed
  showEditModal.value = false
  // Optionally reload or just trust the store update
}

// ---------- Export CSV ----------
const exportToCSV = () => {
  const headers = ['Quotation #', 'Client', 'Amount', 'Status', 'Valid Until', 'Created']
  const rows = sortedQuotations.value.map(q => [
    q.quotation_number,
    q.inquiry_details?.client_details?.name || '',
    q.amount,
    q.status,
    new Date(q.valid_until).toLocaleDateString(),
    new Date(q.created_at).toLocaleDateString()
  ])
  const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.setAttribute('download', 'quotations.csv')
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

// Download PDF for the currently selected quotation
const downloadQuotationPDF = async () => {
  if (!selectedQuotation.value) {
    console.error('No quotation selected')
    return
  }

  const q = selectedQuotation.value
  const client = q.inquiry_details?.client_details || {}
  const amountFormatted = parseFloat(q.amount).toLocaleString()
  const validUntil = new Date(q.valid_until).toLocaleDateString()
  const today = new Date().toLocaleDateString()

  // Build table rows from line_items
  const lineItemsRows = (q.line_items || []).map((item: any) => `
    <tr>
      <td style="padding: 8px 12px; border-bottom: 1px solid #e0e0e0;">${item.service}</td>
      <td style="padding: 8px 12px; border-bottom: 1px solid #e0e0e0; text-align: right;">KSh ${item.price.toLocaleString()}</td>
    </tr>
  `).join('')

  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Quotation ${q.quotation_number}</title>
      <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 30px; background: #f9f9f9; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #e5a233; padding-bottom: 20px; margin-bottom: 30px; }
        .logo img { height: 60px; }
        .title h1 { font-size: 28px; color: #1b325e; margin: 0; }
        .title .ref { font-size: 14px; color: #7f8c8d; margin: 0; }
        .info-row { display: flex; justify-content: space-between; margin-bottom: 25px; padding: 15px; background: #f8fafc; border-radius: 8px; }
        .info-row div { font-size: 14px; }
        .info-row strong { color: #1b325e; }
        .description { margin-bottom: 25px; padding: 15px; background: #f8fafc; border-radius: 8px; }
        .description p { margin: 0; white-space: pre-wrap; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 25px; }
        th { background: #1b325e; color: white; padding: 10px 12px; text-align: left; font-weight: 600; }
        td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; }
        .total-row { background: #f0f4f8; font-weight: bold; }
        .total-row td { border-bottom: none; padding: 12px; }
        .total-row td:last-child { text-align: right; }
        .payment-methods { margin: 20px 0; padding: 15px; background: #f0f4f8; border-radius: 8px; }
        .payment-methods h3 { margin-top: 0; color: #1b325e; }
        .payment-methods ul { list-style: none; padding: 0; display: flex; gap: 20px; flex-wrap: wrap; }
        .payment-methods ul li { font-size: 14px; }
        .terms { margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-size: 12px; color: #555; }
        .footer { margin-top: 30px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #e0e0e0; padding-top: 20px; }
      </style>
    </head>
    <body>
      <div class="container">
        <!-- Header -->
        <div class="header">
          <div class="logo">
            <img src="${window.location.origin}/fix-kraft-logo-white-bg.svg" alt="FixKraft Digital" style="height: 60px;">
          </div>
          <div class="title">
            <h1>QUOTATION</h1>
            <p class="ref">${q.quotation_number}</p>
          </div>
        </div>

        <!-- Client & Date Info -->
        <div class="info-row">
          <div>
            <strong>Client:</strong> ${client.name || '—'}<br>
            <strong>Email:</strong> ${client.email || '—'}<br>
            <strong>Phone:</strong> ${client.phone || '—'}<br>
            <strong>Company:</strong> ${client.company || 'N/A'}
          </div>
          <div style="text-align: right;">
            <strong>Date:</strong> ${today}<br>
            <strong>Valid Until:</strong> ${validUntil}
          </div>
        </div>

        <!-- Description -->
        <div class="description">
          <strong>Description of Work</strong>
          <p>${q.description || '—'}</p>
        </div>

        <!-- Line Items -->
        <table>
          <thead>
            <tr>
              <th>Item</th>
              <th style="text-align: right;">Amount (KSh)</th>
            </tr>
          </thead>
          <tbody>
            ${lineItemsRows}
            <tr class="total-row">
              <td><strong>Total</strong></td>
              <td><strong>${amountFormatted}</strong></td>
            </tr>
          </tbody>
        </table>

        <!-- Payment Methods -->
        <div class="payment-methods">
          <h3>Payment Options</h3>
          <ul>
            <li>🏦 Bank Transfer (Equity, KCB, Co-operative)</li>
            <li>📱 M-Pesa (Paybill: 123456, Account: Invoice #)</li>
            <li>💳 Credit/Debit Card (via PayPal/Stripe)</li>
          </ul>
        </div>

        <!-- Terms -->
        <div class="terms">
          <strong>Terms & Conditions</strong>
          <ul>
            <li>This quotation is valid until ${validUntil}.</li>
            <li>Payment is due within <strong>7 working days</strong> of acceptance.</li>
            <li>All prices are in Kenyan Shillings (KSh).</li>
            <li>Any additional work outside the scope will be quoted separately.</li>
            <li>Please reference quotation number <strong>${q.quotation_number}</strong> in all correspondence.</li>
            <li>For project-based work, a 50% deposit is required before commencement.</li>
          </ul>
        </div>

        <!-- Footer -->
        <div class="footer">
          Thank you for choosing FixKraft Digital.<br>
          📧 info@fixkraftdigital.com &nbsp;|&nbsp; 📞 +254 748 929 891
        </div>
      </div>
    </body>
    </html>
  `

  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = htmlContent
  document.body.appendChild(tempDiv)

  const opt: any = {
    margin: [0.5, 0.5, 0.5, 0.5],
    filename: `Quotation_${q.quotation_number}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
  }

  try {
    await html2pdf().set(opt).from(tempDiv).save()
  } catch (err) {
    console.error('PDF generation failed', err)
  } finally {
    document.body.removeChild(tempDiv)
  }
}

// Email Quotation to client
const emailQuotation = async () => {
  if (!selectedQuotation.value) return
  try {
    const response = await axios.post(`${API_BASE_URI}/quotation/${selectedQuotation.value.id}/email_quotation/`)
    alert('Quotation emailed successfully!')
  } catch (error) {
    console.error('Failed to email quotation', error)
    alert('Failed to send email. Please try again.')
  }
}

const showClientModal = ref(false)
const selectedClient = ref<any>(null)

const openClientDetails = () => {
  if (selectedQuotation.value?.inquiry_details?.client_details) {
    selectedClient.value = selectedQuotation.value.inquiry_details.client_details
    showClientModal.value = true
  }
}

</script>

<template>
  <div class="space-y-8">
    <!-- Header -->
    <PageHeader title="Quotations" subtitle="Manage project quotes and approvals." />

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard title="Total Quotations" :value="totalQuotations" icon="📄" />
      <StatCard title="Total Value" :value="`KSh ${totalAmount.toLocaleString()}`" icon="💰" />
      <StatCard title="Pending Approval" :value="pendingCount" icon="⏳" />
    </div>

    <!-- Search + Filter + Export + Bulk Delete -->
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div class="flex flex-1 gap-3 flex-wrap">
        <input
          v-model="search"
          type="text"
          placeholder="Search by client name or quotation #..."
          class="flex-1 min-w-[200px] px-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary/20"
        />
        <select
          v-model="statusFilter"
          class="px-4 py-3 border rounded-2xl bg-white outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
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
              <tr class="text-left text-sm text-gray-500">
                <th class="px-6 py-4 w-10"><div class="h-4 bg-gray-200 rounded w-5"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-32"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-20"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></th>
                <th class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></th>
                <th class="px-6 py-4 text-right"><div class="h-4 bg-gray-200 rounded w-12 ml-auto"></div></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 5" :key="n" class="border-b">
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-5"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-32"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-36"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-24"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-28"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-24"></div></td>
                <td class="px-6 py-5"><div class="h-5 bg-gray-100 rounded w-16 ml-auto"></div></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div
      v-else-if="sortedQuotations.length"
      class="bg-white rounded-3xl border shadow-sm overflow-hidden"
    >
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr class="text-left text-sm text-gray-500">
              <th class="px-6 py-4 w-10">
                <input type="checkbox" v-model="selectAll" />
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('quotation_number')">
                Quotation #
                <span v-if="sortField === 'quotation_number'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4">Client</th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('amount')">
                Amount (KSh)
                <span v-if="sortField === 'amount'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('status')">
                Status
                <span v-if="sortField === 'status'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 cursor-pointer hover:text-gray-700" @click="toggleSort('valid_until')">
                Valid Until
                <span v-if="sortField === 'valid_until'" class="ml-1">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
              </th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in paginatedQuotations"
              :key="item.id"
              class="border-b last:border-0 hover:bg-gray-50 transition"
            >
              <td class="px-6 py-5">
                <input type="checkbox" :checked="selectedIds.includes(item.id)" @change="toggleSelect(item.id)" />
              </td>
              <td class="px-6 py-5 font-mono text-sm font-medium">
                {{ item.quotation_number }}
              </td>
              <td class="px-6 py-5">
                {{ item.inquiry_details?.client_details?.name || '—' }}
              </td>
              <td class="px-6 py-5">
                {{ parseFloat(item.amount).toLocaleString() }}
              </td>
              <td class="px-6 py-5">
                <span :class="{
                  'bg-yellow-100 text-yellow-700': item.status === 'pending',
                  'bg-green-100 text-green-700': item.status === 'approved',
                  'bg-red-100 text-red-700': item.status === 'rejected'
                }" class="px-2 py-1 rounded-full text-xs">
                  {{ item.status }}
                </span>
              </td>
              <td class="px-6 py-5 text-sm text-gray-500">
                {{ new Date(item.valid_until).toLocaleDateString() }}
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
                    @click="openEditModal(item)"
                    class="px-3 py-2 rounded-xl bg-purple-50 text-purple-600 hover:bg-purple-100 transition text-sm"
                  >
                    Edit
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
          Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, sortedQuotations.length) }} of {{ sortedQuotations.length }} quotations
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

    <!-- Empty -->
    <EmptyState
      v-else
      title="No quotations found"
      message="Create a new quotation from an inquiry to get started."
    />

    <!-- View Modal -->
    <ViewModal :show="showViewModal" title="Quotation Details" @close="showViewModal = false">
      <div class="space-y-4">
        <div><p class="text-sm text-gray-500">Quotation #</p><p class="font-mono">{{ selectedQuotation?.quotation_number }}</p></div>
        <div><p class="text-sm text-gray-500">Client</p><p class="font-medium">{{ selectedQuotation?.inquiry_details?.client_details?.name || '—' }}</p></div>

        <!-- Line items table -->
         <div class="">
            <p class="text-sm text-gray-500">Line Items</p>
            <table class="w-full text-sm mt-1">
                <thead>
                    <tr class="border-b">
                        <th class="text-left py-2">Service</th>
                        <th class="text-right py-2">Price (KSh)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in selectedQuotation?.line_items" :key="item.service" class="border-b">
                        <td class="py-2">{{ item.service }}</td>
                        <td class="text-right py-2">{{ item.price.toLocaleString() }}</td>
                    </tr>
                    <tr>
                        <td class="py-2">Total</td>
                        <td class="text-right py-2">{{ selectedQuotation?.amount ? parseFloat(selectedQuotation.amount).toLocaleString() : '-' }}</td>
                    </tr>
                </tbody>
            </table>
         </div>
        <div><p class="text-sm text-gray-500">Description</p><p class="text-sm">{{ selectedQuotation?.description || '—' }}</p></div>
        <div><p class="text-sm text-gray-500">Valid Until</p><p class="font-medium">{{ selectedQuotation?.valid_until ? new Date(selectedQuotation.valid_until).toLocaleDateString() : '—' }}</p></div>
        <div><p class="text-sm text-gray-500">Status</p><span :class="{
          'bg-yellow-100 text-yellow-700': selectedQuotation?.status === 'pending',
          'bg-green-100 text-green-700': selectedQuotation?.status === 'approved',
          'bg-red-100 text-red-700': selectedQuotation?.status === 'rejected'
        }" class="px-2 py-1 rounded-full text-xs">{{ selectedQuotation?.status }}</span></div>
        <div><p class="text-sm text-gray-500">Created</p><p class="font-medium">{{ selectedQuotation?.created_at ? new Date(selectedQuotation.created_at).toLocaleDateString() : '—' }}</p></div>
      </div>

       <div class="flex gap-2 mt-4">
        <button @click="openClientDetails" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-xl text-sm hover:bg-gray-300">
          👤  View Client
        </button>
        <button @click="downloadQuotationPDF" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">
          📄 Download PDF
        </button>
        <button @click="emailQuotation" class="flex-1 px-4 py-2 bg-green-600 text-white rounded-xl text-sm hover:bg-green-700">
          📧 Email to Client
        </button>
      </div>
    </ViewModal>

    <!-- Client Details Modal -->
    <ViewModal :show="showClientModal" title="Client Details" @close="showClientModal = false">
      <div v-if="selectedClient" class="space-y-3">
        <p><strong>Name:</strong> {{ selectedClient.name }}</p>
        <p><strong>Email:</strong> {{ selectedClient.email }}</p>
        <p><strong>Phone:</strong> {{ selectedClient.phone }}</p>
        <p><strong>Company:</strong> {{ selectedClient.company || 'N/A' }}</p>
        <p><strong>Status:</strong> {{ selectedClient.status }}</p>
        <p><strong>Joined:</strong> {{ new Date(selectedClient.created_at).toLocaleDateString() }}</p>
      </div>
    </ViewModal>

    <!-- Edit Modal -->
    <EditQuotationModal
      :show="showEditModal"
      :quotation="quotationToEdit"
      @close="showEditModal = false"
      @saved="handleEditSaved"
    />

    <!-- Delete Modal -->
    <DeleteModal
      :show="showDeleteModal"
      title="Delete Quotation?"
      message="This quotation will be permanently removed."
      @close="showDeleteModal = false"
      @confirm="deleteConfirmed"
    />
  </div>
</template>
