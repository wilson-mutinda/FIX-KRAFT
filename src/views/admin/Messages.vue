<script setup lang="ts">
import { ref } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'

const activeTab = ref('all')

const messages = ref([
  {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    subject: 'Need a website',
    message:
      'Hello, I need a business website for my startup. I would like to discuss pricing and timelines.',
    unread: true,
    starred: false,
    time: '2m ago'
  },
  {
    id: 2,
    name: 'Mary W.',
    email: 'mary@example.com',
    subject: 'Dashboard redesign',
    message:
      'Can you redesign our current dashboard into a modern SaaS UI?',
    unread: false,
    starred: true,
    time: '1h ago'
  }
])

const selectedMessage = ref(messages.value[0] || null)

const selectMessage = (msg: any) => {
  selectedMessage.value = msg
  msg.unread = false
}
</script>

<template>
  <div class="grid lg:grid-cols-[240px_350px_1fr] gap-6 h-[calc(100vh-140px)]">

    <!-- SIDEBAR -->
    <BaseCard class="space-y-2">

      <h2 class="text-xl font-bold mb-4">
        Inbox
      </h2>

      <button
        @click="activeTab = 'all'"
        class="w-full text-left px-4 py-3 rounded-xl transition"
        :class="activeTab === 'all'
          ? 'bg-primary text-white'
          : 'hover:bg-gray-100'"
      >
        📩 All Messages
      </button>

      <button
        @click="activeTab = 'unread'"
        class="w-full text-left px-4 py-3 rounded-xl transition"
        :class="activeTab === 'unread'
          ? 'bg-primary text-white'
          : 'hover:bg-gray-100'"
      >
        🔵 Unread
      </button>

      <button
        @click="activeTab = 'starred'"
        class="w-full text-left px-4 py-3 rounded-xl transition"
        :class="activeTab === 'starred'
          ? 'bg-primary text-white'
          : 'hover:bg-gray-100'"
      >
        ⭐ Starred
      </button>

    </BaseCard>

    <!-- MESSAGE LIST -->
    <BaseCard class="overflow-y-auto">

      <div class="flex items-center justify-between mb-5">
        <h2 class="font-semibold text-lg">
          Messages
        </h2>

        <BaseBadge color="green">
          {{ messages.length }}
        </BaseBadge>
      </div>

      <div class="space-y-3">

        <div
          v-for="msg in messages"
          :key="msg.id"
          @click="selectMessage(msg)"
          class="p-4 rounded-xl cursor-pointer transition border"
          :class="selectedMessage?.id === msg.id
            ? 'border-primary bg-primary/5'
            : 'border-transparent hover:bg-gray-50'"
        >

          <div class="flex items-center justify-between mb-1">

            <h3 class="font-medium">
              {{ msg.name }}
            </h3>

            <span class="text-xs text-text/50">
              {{ msg.time }}
            </span>

          </div>

          <p class="text-sm font-medium text-text/80">
            {{ msg.subject }}
          </p>

          <p class="text-sm text-text/60 truncate mt-1">
            {{ msg.message }}
          </p>

          <div class="flex items-center gap-2 mt-3">

            <BaseBadge
              v-if="msg.unread"
              color="green"
            >
              Unread
            </BaseBadge>

            <BaseBadge
              v-if="msg.starred"
            >
              Starred
            </BaseBadge>

          </div>

        </div>

      </div>

    </BaseCard>

    <!-- PREVIEW -->
    <BaseCard
      v-if="selectedMessage"
      class="flex flex-col"
    >

      <div class="flex items-start justify-between border-b border-border pb-4">

        <div>
          <h2 class="text-xl font-bold">
            {{ selectedMessage.subject }}
          </h2>

          <p class="text-sm text-text/60 mt-1">
            {{ selectedMessage.name }}
            •
            {{ selectedMessage.email }}
          </p>
        </div>

        <div class="flex gap-2">

          <button class="text-yellow-500 text-xl">
            ⭐
          </button>

          <button class="text-red-500 text-xl">
            🗑️
          </button>

        </div>

      </div>

      <div class="flex-1 py-6 overflow-y-auto">

        <p class="leading-relaxed text-text/80">
          {{ selectedMessage.message }}
        </p>

      </div>

      <div class="border-t border-border pt-4 flex justify-end gap-3">

        <BaseButton variant="secondary">
          Archive
        </BaseButton>

        <BaseButton>
          Reply
        </BaseButton>

      </div>

    </BaseCard>

  </div>
</template>