import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore =
defineStore('toast', () => {

  const show = ref(false)

  const message = ref('')

  const type = ref<
    'success' | 'error'
  >('success')

  const trigger = (
    text: string,
    toastType:
      'success' | 'error'
      = 'success'
  ) => {

    message.value = text

    type.value = toastType

    show.value = true

    setTimeout(() => {

      show.value = false

    }, 3000)
  }

  return {
    show,
    message,
    type,
    trigger
  }
})