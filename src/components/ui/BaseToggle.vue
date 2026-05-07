<script setup lang="ts">
defineProps<{
  modelValue: boolean
}>()

defineEmits(['update:modelValue'])
</script>

<template>
  <button
    @click="$emit('update:modelValue', !modelValue)"
    class="relative inline-flex h-6 w-11 items-center rounded-full transition"
    :class="modelValue ? 'bg-primary' : 'bg-gray-300'"
  >
    <span
      class="inline-block h-4 w-4 transform rounded-full bg-white transition"
      :class="modelValue ? 'translate-x-6' : 'translate-x-1'"
    />
  </button>
</template>