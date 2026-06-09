<template>
    <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="$emit('close')">
        <div class="bg-white rounded-3xl p-6 max-w-md w-full mx-4 shadow-2xl">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold">{{ title }}</h2>
                <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
            </div>

            <!-- slot -->
             <slot />

             <div class="flex justify-end mt-6">
                <button @click="$emit('close')" class="px-5 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition">
                    Close
                </button>
             </div>
        </div>
    </div>
</template>

<script setup lang="ts">

defineProps<{
    show: boolean
    title: string
}>()

defineEmits(['close'])
</script>
