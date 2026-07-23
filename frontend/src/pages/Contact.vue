<script setup lang="ts">
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseTextArea from '@/components/ui/BaseTextArea.vue'
import { API_BASE_URI } from '@/config/api'
import axios from 'axios'
import { ref } from 'vue'

// FORM STATE
const form = ref({
  name: '',
  email: '',
  phone: '',
  company: '',
  services: [] as string[], // multi‑select array
  message: ''
})

const loading = ref(false)
const success = ref(false)
const errorMessage = ref('')

// Service options
const serviceOptions = [
  'Website Development',
  'SaaS Dashboard',
  'Custom CMS',
  'Branding',
  'Mobile App',
  'E‑commerce Solution'
]

// SUBMIT HANDLER
const submitForm = async () => {

  success.value = false
  errorMessage.value = ''

  // Validate required fileds
  if (!form.value.name.trim()) {
    errorMessage.value = 'Please enter your name.';
    return;
  }
  if (!form.value.email.trim()) {
    errorMessage.value = 'Please enter your email.';
    return;
  }
  if (!form.value.phone.trim()) {
    errorMessage.value = 'Please enter your phone number.';
    return;
  }
  if (!form.value.company.trim()) {
    errorMessage.value = 'Please enter your company name.';
    return;
  }
  if (form.value.services.length === 0) {
    errorMessage.value = 'Please select at least one service.';
    return;
  }
  if (!form.value.message.trim()) {
    errorMessage.value = 'Please describe your project.';
    return;
  }

  loading.value = true

  // Convert services array to a comma‑separated string for backend
  const payload = {
    ...form.value,
    service: form.value.services.join(', ')
  }
  delete (payload as any).services // remove the array field

  try {
    await axios.post(`${API_BASE_URI}/inquiries/`, payload)
    success.value = true

    // RESET FORM
    form.value = {
      name: '',
      email: '',
      phone: '',
      company: '',
      services: [],
      message: ''
    }

    setTimeout(() => {
      success.value = false
    }, 6000)
  } catch (error: any) {
    console.error(error)
    let errorMsg = 'Something went wrong. Please try again.'

    const errData = error.response?.data
    if (errData && typeof errData === 'object') {
      // 1. Check for DRF's non_field_errors
      if (errData.non_field_errors && Array.isArray(errData.non_field_errors)) {
        errorMsg = errData.non_field_errors[0]
      }
      // 2. Check for detail (common in DRF)
      else if (errData.detail && typeof errData.detail === 'string') {
        errorMsg = errData.detail
      }
      // 3. Iterate over keys to find the first error message
      else {
        for (const key of Object.keys(errData)) {
          const value = errData[key]
          if (Array.isArray(value) && value.length > 0 && typeof value[0] === 'string') {
            errorMsg = value[0]
            break
          } else if (typeof value === 'string') {
            errorMsg = value
            break
          }
        }
      }
    }
    errorMessage.value = errorMsg
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="bg-white dark:bg-gray-900 min-h-screen">
    <!-- HERO (unchanged) -->
    <section class="py-20 bg-gradient-to-br from-secondary to-black text-white text-center">
      <div class="max-w-3xl mx-auto px-6" data-aos="fade-up">
        <h1 class="text-4xl font-bold mb-4">Let&apos;s Build Something Powerful</h1>
        <p class="text-gray-300">Tell us about your project – we'll get back within 24 hours.</p>
      </div>
    </section>

    <!-- MAIN -->
    <section class="py-20">
      <div class="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-12">
        <!-- LEFT: TRUST + INFO (unchanged) -->
        <div class="space-y-8" data-aos="fade-right">
          <div>
            <h2 class="text-2xl font-bold mb-4 dark:text-white">Why work with FixKraft?</h2>
            <ul class="space-y-3 text-gray-600 dark:text-gray-300 text-sm">
              <li>✔ Custom-built systems (no templates)</li>
              <li>✔ Scalable SaaS-ready architecture</li>
              <li>✔ Clean UI/UX with performance focus</li>
              <li>✔ CMS included for content control</li>
            </ul>
          </div>
          <div>
            <h3 class="font-semibold mb-2 dark:text-white">Contact Info</h3>
            <p class="text-gray-500 dark:text-gray-400 text-sm">info@fixkraftdigital.com</p>
            <p class="text-gray-500 dark:text-gray-400 text-sm">+254 748 929 891</p>
          </div>
          <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-xl text-sm text-gray-600 dark:text-gray-300">
            ⚡ Average response time: <span class="font-semibold">under 24 hours</span>
          </div>
        </div>

        <!-- RIGHT: FORM -->
        <div data-aos="fade-left">
          <form @submit.prevent="submitForm" class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-8 space-y-5 border dark:border-gray-700">
            <h2 class="text-xl font-semibold mb-2">Start Your Project</h2>

            <BaseInput v-model="form.name" placeholder="Your Name" required type="text" />
            <BaseInput v-model="form.email" type="email" placeholder="Your Email" required />
            <BaseInput v-model="form.phone" type="text" placeholder="Phone Number" required />
            <BaseInput v-model="form.company" type="text" placeholder="Company / Business Name" required />

            <!-- Multi‑select services -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Services You Need</label>
              <div class="flex flex-wrap gap-3">
                <label v-for="opt in serviceOptions" :key="opt" class="inline-flex items-center gap-2">
                  <input type="checkbox" v-model="form.services" :value="opt" class="rounded border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                  <span class="text-sm">{{ opt }}</span>
                </label>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-50 mt-1">Select one or more services</p>
            </div>

            <BaseTextArea v-model="form.message" placeholder="Tell us about your project..." rows="4" />

            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-primary text-white py-3 rounded-lg font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed hover:scale-[1.02] active:scale-[0.98]"
            >
              <span v-if="loading">Sending Request...</span>
              <span v-else>Start Project 🚀</span>
            </button>

            <!-- SUCCESS / ERROR messages (unchanged) -->
            <div v-if="success" class="bg-green-50 border border-green-200 rounded-2xl p-5 text-center animate-pulse">
              <div class="text-5xl mb-3">🎉</div>
              <h3 class="text-lg font-semibold text-green-700">Project Request Sent Successfully</h3>
              <p>Thank you for contacting FixKraft Digital. Our team will review your project and respond within 24 hours.</p>
            </div>
            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-2xl p-4 text-sm text-red-600 text-center">
              ⚠ {{ errorMessage }}
            </div>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>
