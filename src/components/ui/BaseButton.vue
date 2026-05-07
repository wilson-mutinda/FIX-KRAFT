<template>
    <button 
    class="px-5 py-2 rounded-xl transition font-medium"
    :class="{
        'bg-primary text-white hover:opacity-90': variant === 'primary' || !variant,
        'bg-gray-100 text-gray-700 hover:bg-gray-200': variant  === 'secondary',
        'bg-red-500 text-white hover:bg-red-600': variant === 'danger'
    }">
        <slot />
    </button>
</template>

<script setup lang="ts">
defineProps<{
    variant?: 'primary' | 'secondary' | 'danger'
}>()
</script>