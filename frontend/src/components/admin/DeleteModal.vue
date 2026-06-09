
<script setup lang="ts">

defineProps<{
    show: boolean
    title?: string
    message?: string
}>()

const emit = defineEmits([
    'close',
    'confirm'
])

</script>

<template>

    <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition duration-150 ease-in"
        leave-to-class="opacity-0 scale-95" 
    >

        <div
         v-if="show" 
         class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" 
         @click.self="emit('close')"
        >

            <div class="w-full max-w-md bg-white rounded-3xl shadow-2xl overflow-hidden">

                <!-- CONTENT -->
                 <div class="p-8 text-center">

                    <!-- ICON -->
                     <div class="w-20 h-20 rounded-full bg-red-100 text-red-500 flex items-center justify-center mx-auto text-4xl">
                        ⚠️
                     </div>

                     <!-- TITLE -->
                      <h2 class="text-2xl font-bold mt-6 text-gray-800">{{ title || 'Delete Item?' }}</h2>

                      <!-- MESAGE -->
                       <p class="text-gray-500 mt-3 leading-relaxed">
                        {{ message || 'This action cannot be undone.' }}
                       </p>

                       <!-- ACTIONS -->
                        <div class="flex gap-3 mt-8">

                            <!-- CANCEL -->
                             <button
                              @click="emit('close')" 
                              class="flex-1 px-5 py-3 rounded-2xl border border-gray-200 hover:bg-gray-50 transition font-medium"
                            >
                                Cancel
                            </button>

                             <!-- DELETE -->
                              <button
                               @click="emit('confirm')" 
                               class="flex-1 px-5 py-3 rounded-2xl bg-red-500 text-white hover:bg-red-600 transition font-medium shadow-lg shadow-red-200"
                               >
                                Delete
                              </button>
                        </div>
                 </div>
            </div>
        </div>
    </transition>
</template>
