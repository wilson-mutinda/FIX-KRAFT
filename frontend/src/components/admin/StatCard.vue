
<script setup lang="ts">
defineProps<{
    title: string
    value: string | number
    icon?: string
}>()
</script>

<template>

    <div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300">

        <div class="flex items-center justify-between">

            <div class="">
                <p class="text-sm text-gray-500">{{ title }}</p>

                <h2 class="text-3xl font-bold mt-2">{{ value }}</h2>
            </div>

            <div class="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-2xl">
                {{ icon }}
            </div>
        </div>
    </div>
</template>