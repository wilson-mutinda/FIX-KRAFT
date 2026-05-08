<script setup lang="ts">
import { ref, onMounted } from 'vue'

import { useProjectsStore } from '@/stores/projects'
import { useToastStore } from '@/stores/toast'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'

const store = useProjectsStore()
const toast = useToastStore()

// LOAD PROJECTS
onMounted(() => {
  store.load()
})

// FORM
const newProject = ref({
  title: '',
  category: '',
  image: '' as string | null
})

// LOADING
const loading = ref(false)

// EDIT MODE
const editingId = ref<number | null>(null)

// DELETE MODAL
const showDelete = ref(false)
const selectedDeleteId = ref<number | null>(null)

// IMAGE UPLOAD
const uploadImage = (
  e: Event
) => {

  const target =
    e.target as HTMLInputElement

  if (!target.files?.length)
    return

  const file = target.files[0]

  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {

    newProject.value.image =
      reader.result as string
  }

  reader.readAsDataURL(file)
}

// ADD / UPDATE
const saveProject = async () => {

  if (
    !newProject.value.title ||
    !newProject.value.image
  ) {

    toast.trigger(
      'Title and image are required',
      'error'
    )

    return
  }

  loading.value = true

  setTimeout(() => {

    if (editingId.value) {

      store.updateProject(
        editingId.value,
        {
          ...newProject.value
        }
      )

      toast.trigger(
        'Project updated successfully'
      )

    } else {

      store.addProject({
        ...newProject.value
      })

      toast.trigger(
        'Project added successfully'
      )
    }

    resetForm()

    loading.value = false

  }, 1200)
}

// RESET
const resetForm = () => {

  newProject.value = {
    title: '',
    category: '',
    image: ''
  }

  editingId.value = null
}

// EDIT
const editProject = (
  project: any
) => {

  newProject.value = {
    title: project.title,
    category: project.category,
    image: project.image
  }

  editingId.value = project.id

  toast.trigger(
    'Editing project'
  )
}

// OPEN DELETE
const openDelete = (
  id: number
) => {

  selectedDeleteId.value = id

  showDelete.value = true
}

// CONFIRM DELETE
const confirmDelete = () => {

  if (!selectedDeleteId.value)
    return

  store.deleteProject(
    selectedDeleteId.value
  )

  toast.trigger(
    'Project deleted',
    'error'
  )

  showDelete.value = false
}
</script>

<template>
  <div class="space-y-8">

    <!-- HEADER -->
    <div class="flex items-center justify-between">

      <div>
        <h1 class="text-3xl font-bold">
          Projects Manager
        </h1>

        <p class="text-gray-500 mt-1">
          Manage your portfolio projects
        </p>
      </div>

      <BaseButton>
        + New Project
      </BaseButton>

    </div>

    <!-- FORM -->
    <div
      class="bg-white border border-gray-100
             rounded-3xl p-6 shadow-sm
             space-y-5"
    >

      <div class="grid md:grid-cols-2 gap-5">

        <BaseInput
          v-model="newProject.title"
          placeholder="Project title"
        />

        <BaseInput
          v-model="newProject.category"
          placeholder="Project category"
        />

      </div>

      <!-- UPLOAD -->
      <div class="space-y-3">

        <label
          class="border-2 border-dashed
                 rounded-2xl p-8
                 flex flex-col items-center
                 justify-center cursor-pointer
                 hover:border-primary transition"
        >

          <div class="text-4xl mb-3">
            🖼️
          </div>

          <p class="font-medium">
            Upload Project Image
          </p>

          <p class="text-sm text-gray-500 mt-1">
            PNG, JPG or WEBP
          </p>

          <input
            type="file"
            accept="image/*"
            class="hidden"
            @change="uploadImage"
          />

        </label>

        <!-- PREVIEW -->
        <div
          v-if="newProject.image"
          class="rounded-2xl overflow-hidden border"
        >

          <img
            :src="newProject.image"
            class="h-64 w-full object-cover"
          />

        </div>

      </div>

      <!-- ACTIONS -->
      <div class="flex gap-3 justify-end">

        <BaseButton
          variant="secondary"
          @click="resetForm"
        >
          Cancel
        </BaseButton>

        <BaseButton
          @click="saveProject"
          :disabled="loading"
          class="flex items-center gap-2"
        >

          <span
            v-if="loading"
            class="w-4 h-4 border-2
                   border-white border-t-transparent
                   rounded-full animate-spin"
          />

          {{
            loading
              ? 'Saving...'
              : editingId
                ? 'Update Project'
                : 'Save Project'
          }}

        </BaseButton>

      </div>

    </div>

    <!-- EMPTY STATE -->
    <div
      v-if="!store.projects.length"
      class="bg-white border rounded-3xl
             py-24 text-center"
    >

      <div class="text-6xl mb-5">
        📂
      </div>

      <h2 class="text-2xl font-bold mb-2">
        No Projects Yet
      </h2>

      <p class="text-gray-500">
        Start by creating your first project.
      </p>

    </div>

    <!-- PROJECTS GRID -->
    <div
      v-else
      class="grid md:grid-cols-2 xl:grid-cols-3 gap-6"
    >

      <div
        v-for="p in store.projects"
        :key="p.id"
        class="group bg-white rounded-3xl
               overflow-hidden shadow-sm
               hover:shadow-xl transition"
      >

        <!-- IMAGE -->
        <div class="relative overflow-hidden">

          <img
            :src="p.image"
            class="h-56 w-full object-cover
                   group-hover:scale-105
                   transition duration-500"
          />

          <div
            class="absolute inset-0
                   bg-black/0 group-hover:bg-black/20
                   transition"
          />

        </div>

        <!-- CONTENT -->
        <div class="p-5">

          <div class="flex items-start justify-between">

            <div>
              <h3 class="font-bold text-lg">
                {{ p.title }}
              </h3>

              <p class="text-sm text-gray-500 mt-1">
                {{ p.category }}
              </p>
            </div>

            <div class="text-xl">
              🚀
            </div>

          </div>

          <!-- ACTIONS -->
          <div class="flex gap-3 mt-6">

            <button
              @click="editProject(p)"
              class="flex-1 py-2 rounded-xl
                     bg-primary/10 text-primary
                     hover:bg-primary hover:text-white
                     transition"
            >
              Edit
            </button>

            <button
              @click="openDelete(p.id)"
              class="flex-1 py-2 rounded-xl
                     bg-red-50 text-red-500
                     hover:bg-red-500 hover:text-white
                     transition"
            >
              Delete
            </button>

          </div>

        </div>

      </div>

    </div>

    <!-- DELETE MODAL -->
    <BaseModal
      :show="showDelete"
      @close="showDelete = false"
    >

      <h2 class="text-2xl font-bold mb-3">
        Delete Project?
      </h2>

      <p class="text-gray-500">
        This action cannot be undone.
      </p>

      <div class="flex justify-end gap-3 mt-8">

        <button
          @click="showDelete = false"
          class="px-5 py-2 rounded-xl
                 bg-gray-100"
        >
          Cancel
        </button>

        <button
          @click="confirmDelete"
          class="px-5 py-2 rounded-xl
                 bg-red-500 text-white"
        >
          Delete
        </button>

      </div>

    </BaseModal>

  </div>
</template>