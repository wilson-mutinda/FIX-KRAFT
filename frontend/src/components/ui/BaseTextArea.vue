<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
}>()

defineEmits(['update:modelValue'])
</script>

<template>
  <textarea
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    :placeholder="placeholder"
    rows="5"
    class="w-full px-4 py-3 border border-border rounded-xl
           bg-transparent outline-none
           focus:ring-2 focus:ring-primary/20"
  />
</template>