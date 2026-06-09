<script setup lang="ts">
defineProps<{
  color?: 'green' | 'red' | 'gray'
}>()
</script>

<template>
  <span
    class="px-3 py-1 rounded-full text-xs font-medium"
    :class="{
      'bg-green-100 text-green-700': color === 'green',
      'bg-red-100 text-red-700': color === 'red',
      'bg-gray-100 text-gray-700': !color || color === 'gray',
    }"
  >
    <slot />
  </span>
</template>