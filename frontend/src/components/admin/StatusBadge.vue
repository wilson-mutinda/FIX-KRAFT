
<script setup lang="ts">
import { computed } from 'vue';


const props = defineProps<{
    status: string
}>()

const badgeClass = computed(() => {

    switch (props.status) {
        case 'new':
            return 'bg-blue-100 text-blue-700'

        case 'quoted':
            return 'bg-yellow-100 text-yellow-700'

        case 'in_progress':
            return 'bg-purple-100 text-purple-700'

        case 'completed':
            return 'bg-green-100 text-green-700'

        case 'cancelled':
            return 'bg-red-100 text-red-700'

        default:
            return 'bg-gray-100 text-gray-700'
    }
})
</script>

<template>

    <span :class="[
        badgeClass, 'px-3 py-1 rounded-full text-xs font-semibold capitalize'
    ]">
        {{ status.replace('_', ' ') }}
    </span>
</template>