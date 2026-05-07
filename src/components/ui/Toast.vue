<script setup lang="ts">
defineProps<{
  message: string
  type?: string
}>()
</script>

<template>
  <div
    class="px-5 py-3 rounded-xl shadow-lg text-white"
    :class="{
      'bg-green-500': type === 'success',
      'bg-red-500': type === 'error',
      'bg-blue-500': type === 'info',
    }"
  >
    {{ message }}
  </div>
</template>