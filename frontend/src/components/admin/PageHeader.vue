
<script setup lang="ts">

defineProps<{
    title: string
    subtitle?: string
}>()
</script>

<template>
    
    <div class="mb-8">

        <h1 class="text-3xl font-bold tracking-tight">{{ title }}</h1>

        <p v-if="subtitle" class="text-gray-500 mt-2">{{ subtitle }}</p>

    </div>
</template>
