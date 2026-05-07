<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useServicesStore } from '@/stores/services'

const store = useServicesStore()

const selected = ref<any>(null)

onMounted(() => {
  store.load()
})

const selectService = (s: any) => {
  selected.value = { ...s }
}

const save = () => {
  store.update(selected.value)
  alert('Saved!')
}

const addNew = () => {
  const newService = {
    id: Date.now(),
    title: 'New Service',
    description: '',
    image: '',
    features: []
  }

  store.services.push(newService)
  selected.value = newService
}

const uploadImage = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0]

    if (!file || !selected.value) return

    const reader = new FileReader()

    reader.onload = () => {
        selected.value.image = reader.result as string
    }

    reader.readAsDataURL(file)
}

</script>

<template>
  <div class="flex gap-6">

    <!-- LEFT: LIST -->
    <div class="w-1/3 bg-white p-4 rounded-xl shadow space-y-3">

      <button
        @click="addNew"
        class="bg-primary text-white px-3 py-2 rounded w-full"
      >
        + New Service
      </button>

      <div
        v-for="s in store.services"
        :key="s.id"
        @click="selectService(s)"
        class="p-3 border rounded cursor-pointer hover:bg-gray-50"
      >
        {{ s.title }}
      </div>

    </div>

    <!-- RIGHT: EDITOR -->
    <div class="flex-1 bg-white p-6 rounded-xl shadow" v-if="selected">

      <h2 class="text-xl font-bold mb-4">Edit Service</h2>

      <input v-model="selected.title" class="input mb-3" placeholder="Title" />

      <textarea
        v-model="selected.description"
        class="input mb-3"
        placeholder="Description"
      />

      <!-- IMAGE UPLOAD -->
      <input type="file" @change="(e) => uploadImage(e)" />

      <img v-if="selected.image" :src="selected.image" class="h-32 mt-2" />

      <!-- FEATURES -->
      <div class="mt-4">
        <p class="font-medium mb-2">Features</p>

        <div v-for="(f, i) in selected.features" :key="i" class="flex gap-2 mb-2">
          <input v-model="selected.features[i]" class="input flex-1" />
          <button @click="selected.features.splice(i,1)">❌</button>
        </div>

        <button @click="selected.features.push('')" class="text-primary text-sm">
          + Add Feature
        </button>
      </div>

      <button
        @click="save"
        class="mt-6 bg-primary text-white px-5 py-2 rounded"
      >
        Save Service
      </button>

    </div>

  </div>
</template>