<script setup lang="ts">
import { ref } from 'vue'

const images = ref<string[]>([])

const upload = (
  e: Event
) => {

  const target =
    e.target as HTMLInputElement

  if (!target.files || !target.files.length)
    return

  const file = target.files[0]

  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {

    images.value.push(
      reader.result as string
    )
  }

  reader.readAsDataURL(file)
}
</script>

<template>

  <div class="space-y-6">

    <!-- HEADER -->
    <div class="flex items-center justify-between">

      <div>
        <h2 class="text-2xl font-bold">
          Media Manager
        </h2>

        <p class="text-sm text-gray-500 mt-1">
          Upload and manage your images
        </p>
      </div>

      <label
        class="bg-primary text-white
               px-5 py-3 rounded-xl
               cursor-pointer hover:opacity-90 transition"
      >
        Upload Image

        <input
          type="file"
          class="hidden"
          accept="image/*"
          @change="upload"
        >
      </label>

    </div>

    <!-- EMPTY STATE -->
    <div
        v-if="!images.length"
        class="border border-dashed border-border
                rounded-3xl py-24 text-center"
        >

        <div class="text-7xl mb-5">
            🖼️
        </div>

        <h2 class="text-2xl font-bold mb-3">
            No Media Uploaded
        </h2>

        <p class="text-text/60 max-w-md mx-auto mb-6">
            Upload logos, project banners, and portfolio images.
        </p>

        <label
            class="inline-flex items-center gap-2
                bg-primary text-white
                px-6 py-3 rounded-xl
                cursor-pointer hover:opacity-90 transition"
        >

            📤 Upload Media

            <input
            type="file"
            class="hidden"
            @change="upload"
            >

        </label>

    </div>

    <!-- GRID -->
    <div
      v-else
      class="grid grid-cols-2 md:grid-cols-4 gap-5"
    >

      <div
        v-for="img in images"
        :key="img"
        class="group relative aspect-square
               rounded-3xl overflow-hidden border"
      >

        <img
          :src="img"
          class="w-full h-full object-cover
                 group-hover:scale-105 transition duration-300"
        >

      </div>

    </div>
    
  </div>

</template>