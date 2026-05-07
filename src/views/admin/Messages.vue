<script setup lang="ts">
import { ref, onMounted } from 'vue'

// TEMP STORE (replace with Pinia later)
const messages = ref<any[]>([])
const selected = ref<any>(null)

onMounted(() => {
  const saved = localStorage.getItem('messages')
  if (saved) messages.value = JSON.parse(saved)
})

// SELECT MESSAGE
const selectMessage = (msg: any) => {
  selected.value = msg
  msg.read = true
  save()
}

// DELETE
const remove = (id: number) => {
  messages.value = messages.value.filter(m => m.id !== id)
  if (selected.value?.id === id) selected.value = null
  save()
}

// SAVE
const save = () => {
  localStorage.setItem('messages', JSON.stringify(messages.value))
}
</script>

<template>
  <div class="flex gap-6 h-full">

    <!-- LEFT: MESSAGE LIST -->
    <div class="w-1/3 bg-white rounded-xl shadow p-4 overflow-y-auto">

      <h2 class="text-lg font-semibold mb-4">Messages</h2>

      <div
        v-for="msg in messages"
        :key="msg.id"
        @click="selectMessage(msg)"
        class="p-3 border rounded-lg mb-2 cursor-pointer transition hover:bg-gray-50"
        :class="!msg.read ? 'border-primary bg-primary/5' : ''"
      >
        <p class="font-medium">{{ msg.name }}</p>
        <p class="text-xs text-gray-500 truncate">
          {{ msg.message }}
        </p>
      </div>

      <p v-if="messages.length === 0" class="text-sm text-gray-400">
        No messages yet
      </p>

    </div>

    <!-- RIGHT: MESSAGE VIEW -->
    <div class="flex-1 bg-white rounded-xl shadow p-6" v-if="selected">

      <div class="flex justify-between items-start mb-4">
        <div>
          <h2 class="text-xl font-bold">{{ selected.name }}</h2>
          <p class="text-sm text-gray-500">{{ selected.email }}</p>
        </div>

        <button
          @click="remove(selected.id)"
          class="text-red-500 text-sm"
        >
          Delete
        </button>
      </div>

      <div class="space-y-4">
        <p class="text-gray-700">
          {{ selected.message }}
        </p>
      </div>

    </div>

    <!-- EMPTY STATE -->
    <div v-else class="flex-1 flex items-center justify-center text-gray-400">
      Select a message to read
    </div>

  </div>
</template>