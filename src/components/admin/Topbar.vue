<script setup lang="ts">
const emit = defineEmits(['toggle-sidebar'])
</script>

<template>
  <header class="h-16 bg-white border-b flex items-center justify-between px-6">

    <!-- LEFT -->
    <div class="flex items-center gap-4">

      <button
        @click="emit('toggle-sidebar')"
        class="p-2 rounded-lg hover:bg-gray-100"
      >
        ☰
      </button>

      <h1 class="font-semibold text-gray-700">
        Admin Panel
      </h1>

    </div>

    <!-- RIGHT -->
    <div class="flex items-center gap-4">

      <span class="text-sm text-gray-500">
        Admin
      </span>

      <div class="h-8 w-8 bg-gray-300 rounded-full"></div>

    </div>

  </header>
</template>