<script setup lang="ts">
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
</script>

<template>

  <transition
    enter-active-class="transition duration-300"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition duration-300"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >

    <div
      v-if="toast.show"
      class="fixed top-6 right-6 z-50
             px-5 py-4 rounded-2xl shadow-2xl
             text-white font-medium backdrop-blur-lg"
      :class="toast.type === 'success'
        ? 'bg-green-500'
        : 'bg-red-500'"
    >

      {{ toast.message }}

    </div>

  </transition>

</template>