<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white rounded-3xl p-6 max-w-md w-full mx-4 shadow-2xl">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Edit Quotation</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Quotation Number</label>
          <input
            v-model="form.quotation_number"
            type="text"
            class="w-full border rounded-2xl px-4 py-2 outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Amount (KSh)</label>
          <input
            v-model="form.amount"
            type="text"
            step="0.01"
            class="w-full border rounded-2xl px-4 py-2 outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full border rounded-2xl px-4 py-2 outline-none focus:ring-2 focus:ring-primary/20"
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Valid Until</label>
          <input
            v-model="form.valid_until"
            type="date"
            class="w-full border rounded-2xl px-4 py-2 outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            v-model="form.status"
            class="w-full border rounded-2xl px-4 py-2 outline-none focus:ring-2 focus:ring-primary/20"
          >
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end gap-3 mt-6">
        <button
          @click="$emit('close')"
          class="px-5 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition"
        >
          Cancel
        </button>
        <button
          @click="save"
          :disabled="saving"
          class="px-5 py-2 rounded-xl bg-primary text-white hover:opacity-90 transition disabled:opacity-50"
        >
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useQuotationStore } from '@/stores/quotation'

const props = defineProps<{
  show: boolean
  quotation: any | null
}>()

const emit = defineEmits(['close', 'saved'])

const store = useQuotationStore()
const saving = ref(false)

// Form fields now match the Quotation interface types
const form = ref({
  quotation_number: '',
  amount: '',        // string to match backend decimal as string
  description: '',
  valid_until: '',
  status: 'pending' as 'pending' | 'approved' | 'rejected'
})

watch(() => props.quotation, (newVal) => {
  if (newVal) {
    form.value = {
      quotation_number: newVal.quotation_number || '',
      amount: newVal.amount?.toString() || '0',
      description: newVal.description || '',
      valid_until: newVal.valid_until?.split('T')[0] || '',
      status: newVal.status || 'pending'
    }
  }
}, { immediate: true })

const save = async () => {
  if (!props.quotation) return
  saving.value = true
  try {
    // Payload directly matches the store's update expected type
    const payload = {
      quotation_number: form.value.quotation_number,
      amount: form.value.amount,
      description: form.value.description,
      valid_until: form.value.valid_until,
      status: form.value.status
    }
    await store.update(props.quotation.id, payload)
    emit('saved')
    emit('close')
  } catch (error) {
    console.error('Update failed', error)
  } finally {
    saving.value = false
  }
}
</script>