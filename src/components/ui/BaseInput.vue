<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
}>()

defineEmits(['update:modelValue'])
</script>

<template>
  <input
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    :placeholder="placeholder"
    class="w-full px-4 py-3 border border-border rounded-xl
           bg-transparent outline-none
           focus:ring-2 focus:ring-primary/20"
  />
</template>
