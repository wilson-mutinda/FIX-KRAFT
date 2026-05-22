<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
  watch
} from 'vue'
import { debounce } from 'lodash-es'

import { useMediaStore } from '@/stores/media'
import { useCategoryStore } from '@/stores/category'

const store = useMediaStore()
const categoryStore = useCategoryStore()

// ========== State ==========
const loading = ref(false)
const title = ref('')
const description = ref('')
const selectedCategory = ref<number | null>(null)
const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

// Filters
const activeCategory = ref<string>('All')
const searchQuery = ref('')
const debouncedQuery = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 12

// Delete modal
const showDeleteModal = ref(false)
const itemToDelete = ref<number | null>(null)

// Lightbox
const lightboxImage = ref<string | null>(null)

// Toast
const toast = ref<{ message: string; type: 'success' | 'error' } | null>(null)

// ========== Helpers ==========
const showToast = (message: string, type: 'success' | 'error') => {
  toast.value = { message, type }
  setTimeout(() => {
    toast.value = null
  }, 3000)
}

// Debounced search
const updateDebounced = debounce((val: string) => {
  debouncedQuery.value = val
  currentPage.value = 1
}, 300)

watch(searchQuery, (newVal) => updateDebounced(newVal))

// ========== Lifecycle ==========
onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([store.load(), categoryStore.load()])
  } finally {
    loading.value = false
  }
})

// ========== File handling ==========
const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0] || null
  selectedFile.value = file

  if (file) {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = URL.createObjectURL(file)
  } else {
    previewUrl.value = null
  }
}

// ========== Upload ==========
const upload = async () => {
  if (!selectedFile.value) return

  loading.value = true
  try {
    await store.upload(
      selectedFile.value,
      title.value,
      description.value,
      selectedCategory.value
    )

    // Reset form
    title.value = ''
    description.value = ''
    selectedCategory.value = null
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value)
      previewUrl.value = null
    }
    selectedFile.value = null

    showToast('Uploaded successfully!', 'success')
  } catch (err) {
    console.error(err)
    showToast('Upload failed. Please try again.', 'error')
  } finally {
    loading.value = false
  }
}

// ========== Delete modal ==========
const confirmDelete = (id: number) => {
  itemToDelete.value = id
  showDeleteModal.value = true
}

const deleteConfirmed = async () => {
  if (!itemToDelete.value) return
  try {
    await store.remove(itemToDelete.value)
    showToast('Deleted successfully', 'success')
  } catch (err) {
    console.error(err)
    showToast('Delete failed', 'error')
  } finally {
    showDeleteModal.value = false
    itemToDelete.value = null
  }
}

// ========== Filters ==========
const clearFilters = () => {
  activeCategory.value = 'All'
  searchQuery.value = ''
  debouncedQuery.value = ''
  currentPage.value = 1
}

const filteredMedia = computed(() => {
  let filtered = store.media

  // Category filter
  if (activeCategory.value !== 'All') {
    filtered = filtered.filter(
      item => item.category_details?.name === activeCategory.value
    )
  }

  // Search filter
  if (debouncedQuery.value.trim()) {
    const query = debouncedQuery.value.toLowerCase()
    filtered = filtered.filter(
      item =>
        item.title?.toLowerCase().includes(query) ||
        item.description?.toLowerCase().includes(query) ||
        item.category_details?.name?.toLowerCase().includes(query)
    )
  }

  return filtered
})

// ========== Pagination ==========
const paginatedMedia = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredMedia.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(filteredMedia.value.length / itemsPerPage))

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>

<template>
  <div class="space-y-8">
    <!-- Toast Notification -->
    <div
      v-if="toast"
      class="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-5 fade-in duration-300"
    >
      <div
        :class="[
          'px-6 py-3 rounded-2xl shadow-lg text-white font-medium',
          toast.type === 'success' ? 'bg-green-600' : 'bg-red-600'
        ]"
      >
        {{ toast.message }}
      </div>
    </div>

    <!-- Header -->
    <div class="flex flex-col gap-5">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Media Manager</h1>
        <p class="text-gray-500 mt-2">
          Manage uploaded assets, project banners, portfolio images and logos.
        </p>
      </div>

      <!-- Upload Card -->
      <div class="bg-white border rounded-3xl p-6 space-y-4 shadow-sm">
        <input
          v-model="title"
          type="text"
          placeholder="Enter image title"
          class="w-full border rounded-2xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition"
        />

        <select
          v-model="selectedCategory"
          class="w-full border rounded-2xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option :value="null">Select Category</option>
          <option v-for="cat in categoryStore.categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>

        <textarea
          v-model="description"
          rows="4"
          placeholder="Enter description"
          class="w-full border rounded-2xl px-4 py-3 outline-none focus:ring-2 focus:ring-primary/20"
        />

        <input
          type="file"
          accept="image/*"
          @change="onFileChange"
          class="w-full border rounded-2xl px-4 py-3 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-primary/10 file:text-primary file:font-medium hover:file:bg-primary/20 transition"
        />

        <!-- Preview -->
        <div v-if="previewUrl" class="mt-2 flex items-center gap-4">
          <img :src="previewUrl" class="w-20 h-20 object-cover rounded-xl border shadow-sm" />
          <button
            @click="previewUrl = null; selectedFile = null"
            class="text-sm text-red-500 hover:underline"
          >
            Remove
          </button>
        </div>

        <button
          @click="upload"
          :disabled="!selectedFile"
          class="bg-primary text-white px-6 py-3 rounded-2xl shadow-lg hover:opacity-90 transition disabled:opacity-40 disabled:cursor-not-allowed"
        >
          Upload Media
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="bg-white border rounded-3xl p-6 flex items-center justify-between shadow-sm">
      <div>
        <p class="text-sm text-gray-500">Total Files</p>
        <h2 class="text-3xl font-bold mt-1">{{ store.media.length }}</h2>
      </div>
      <div class="text-5xl">🖼️</div>
    </div>

    <!-- Loading State (Skeleton) -->
    <div v-if="loading" class="space-y-6">
      <div class="bg-white rounded-3xl border p-4">
        <div class="h-12 bg-gray-100 rounded-2xl animate-pulse"></div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
        <div v-for="n in 8" :key="n" class="bg-white border rounded-3xl overflow-hidden shadow-sm">
          <div class="aspect-square bg-gray-100 animate-pulse"></div>
          <div class="p-4 space-y-3">
            <div class="h-4 bg-gray-100 rounded-full w-3/4 animate-pulse"></div>
            <div class="h-3 bg-gray-100 rounded-full w-1/2 animate-pulse"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State (No Media at All) -->
    <div
      v-else-if="!store.media.length"
      class="bg-white border border-dashed rounded-3xl py-24 text-center"
    >
      <div class="text-7xl mb-5">📭</div>
      <h2 class="text-2xl font-bold">No Media Uploaded</h2>
      <p class="text-gray-500 max-w-md mx-auto mt-3">
        Upload logos, banners, thumbnails and project assets using the form above.
      </p>
    </div>

    <!-- Search & Filters (only shown if media exists) -->
    <div v-else>
      <div class="bg-white border rounded-3xl p-4 shadow-sm">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by title, description or category..."
          class="w-full px-4 py-3 border rounded-2xl outline-none focus:ring-2 focus:ring-primary/20"
        />
      </div>

      <!-- Category Filters + Clear Button -->
      <div class="flex flex-wrap items-center justify-between gap-3 my-6">
        <div class="flex flex-wrap gap-3">
          <button
            @click="activeCategory = 'All'"
            :class="[
              activeCategory === 'All'
                ? 'bg-primary text-white'
                : 'bg-white border hover:bg-gray-50',
              'px-5 py-2 rounded-2xl transition shadow-sm'
            ]"
          >
            All
          </button>
          <button
            v-for="cat in categoryStore.categories"
            :key="cat.id"
            @click="activeCategory = cat.name"
            :class="[
              activeCategory === cat.name
                ? 'bg-primary text-white'
                : 'bg-white border hover:bg-gray-50',
              'px-5 py-2 rounded-2xl transition shadow-sm'
            ]"
          >
            {{ cat.name }}
          </button>
        </div>
        <button
          v-if="activeCategory !== 'All' || searchQuery"
          @click="clearFilters"
          class="text-sm text-primary hover:underline px-3 py-1"
        >
          Clear filters ✕
        </button>
      </div>

      <!-- Media Grid -->
      <div v-if="filteredMedia.length" class="space-y-6">
        <div
          class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          <div
            v-for="item in paginatedMedia"
            :key="item.id"
            class="group relative bg-white border rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300"
          >
            <!-- Image with click to lightbox -->
            <div class="aspect-square overflow-hidden cursor-pointer" @click="lightboxImage = item.file">
              <img
                :src="item.file"
                class="w-full h-full object-cover group-hover:scale-105 transition duration-500"
              />
            </div>

            <!-- Delete button (hover) -->
            <div
              class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition"
            >
              <button
                @click="confirmDelete(item.id)"
                class="bg-red-500 text-white px-4 py-2 rounded-xl shadow-lg hover:bg-red-600 transition"
              >
                Delete
              </button>
            </div>

            <!-- Footer -->
            <div class="p-4">
              <p class="text-sm font-medium truncate">
                {{ item.title || 'Untitled Image' }}
              </p>
              <div class="flex items-center justify-between mt-3">
                <span class="text-xs bg-primary/10 text-primary px-3 py-1 rounded-full">
                  {{ item.category_details?.name || 'Uncategorized' }}
                </span>
              </div>
              <p class="text-xs text-gray-500 mt-2 line-clamp-2">
                {{ item.description || 'No description' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex justify-center gap-2 pt-4">
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-4 py-2 rounded-xl border bg-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 transition"
          >
            ← Prev
          </button>
          <span class="px-4 py-2 text-sm text-gray-600">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-4 py-2 rounded-xl border bg-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 transition"
          >
            Next →
          </button>
        </div>
      </div>

      <!-- No Results (filtered empty) -->
      <div v-else class="bg-white border rounded-3xl py-20 text-center">
        <div class="text-6xl mb-4">🔍</div>
        <h2 class="text-2xl font-bold">No matching media</h2>
        <p class="text-gray-500 mt-3">Try another search or category.</p>
        <button @click="clearFilters" class="mt-4 text-primary underline">Clear all filters</button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white rounded-3xl p-6 max-w-sm w-full mx-4 shadow-2xl">
        <div class="text-center">
          <div class="text-5xl mb-3">⚠️</div>
          <h3 class="text-xl font-bold">Delete image?</h3>
          <p class="text-gray-500 mt-2">This action cannot be undone.</p>
          <div class="flex gap-3 mt-6">
            <button
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 border rounded-xl hover:bg-gray-50 transition"
            >
              Cancel
            </button>
            <button
              @click="deleteConfirmed"
              class="flex-1 px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <div
      v-if="lightboxImage"
      class="fixed inset-0 bg-black/90 flex items-center justify-center z-50 cursor-pointer"
      @click="lightboxImage = null"
    >
      <img :src="lightboxImage" class="max-w-[90vw] max-h-[90vh] object-contain rounded-2xl shadow-2xl" />
      <button class="absolute top-4 right-4 text-white text-4xl">&times;</button>
    </div>
  </div>
</template>