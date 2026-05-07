<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProjectsStore } from '@/stores/projects'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const store = useProjectsStore()

const newProject = ref({
  title: '',
  category: '',
  image: '' as string | null,
})

const uploadImage = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0]

    if (!file) return

    const reader = new FileReader()

    reader.onload = () => {
        newProject.value.image = reader.result as string
    }

    reader.readAsDataURL(file)
}

onMounted(() => {
  store.load()
})

const add = () => {
  if (!newProject.value.title || !newProject.value.image) {
    alert('Title and image are required')
    return
  }

  store.addProject({ ...newProject.value })

  newProject.value = {
    title: '',
    category: '',
    image: ''
  }
}

</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Projects Manager</h2>

    <!-- ADD FORM -->
    <div class="bg-white p-6 rounded-xl shadow mb-6 space-y-3">

        <!-- <input v-model="newProject.title" placeholder="Title" class="input" /> -->
        <BaseInput v-model="newProject.title" placeholder="Title" />

        <!-- <input v-model="newProject.category" placeholder="Category" class="input" /> -->
         <BaseInput v-model="newProject.category" placeholder="Category" />

        <input type="file" accept="image/*" @change="uploadImage" />

        <!-- PREVIEW -->
        <div v-if="newProject.image">
            <img :src="newProject.image" class="h-40 w-full object-cover rounded" />
        </div>

        <BaseButton @click="add">
          Add Project
        </BaseButton>

    </div>

    <!-- LIST -->
    <div class="grid md:grid-cols-3 gap-6">
      <div v-for="p in store.projects" :key="p.id" class="bg-white p-4 rounded-xl shadow">
        <img :src="p.image" class="h-40 w-full object-cover rounded mb-2" />
        <h3 class="font-semibold">{{ p.title }}</h3>
        <p class="text-sm text-gray-500">{{ p.category }}</p>

        <button
          @click="store.deleteProject(p.id)"
          class="text-red-500 text-sm mt-2"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>