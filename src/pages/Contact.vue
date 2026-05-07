<script setup lang="ts">
import BaseInput from '@/components/ui/BaseInput.vue'
import { ref } from 'vue'

// FORM STATE
const form = ref({
  name: '',
  email: '',
  service: '',
  budget: '',
  message: ''
})

const loading = ref(false)
const success = ref(false)

// SUBMIT HANDLER (ready for backend)
const submitForm = async () => {
  loading.value = true

  try {
    // 🔥 Replace with API later
    console.log('Form Data:', form.value)

    await new Promise(resolve => setTimeout(resolve, 1500)) // simulate API

    success.value = true

    // reset
    form.value = {
      name: '',
      email: '',
      service: '',
      budget: '',
      message: ''
    }

  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="bg-white min-h-screen">

    <!-- HERO -->
    <section class="py-20 bg-gradient-to-br from-secondary to-black text-white text-center">
      <div class="max-w-3xl mx-auto px-6" data-aos="fade-up">

        <h1 class="text-4xl font-bold mb-4">
          Let&apos;s Build Something Powerful
        </h1>

        <p class="text-gray-300">
          Tell us about your project and we&apos;ll get back within 24 hours.
        </p>

      </div>
    </section>

    <!-- MAIN -->
    <section class="py-20">
      <div class="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-12">

        <!-- LEFT: TRUST + INFO -->
        <div class="space-y-8" data-aos="fade-right">

          <div>
            <h2 class="text-2xl font-bold mb-4">
              Why work with FixKraft?
            </h2>

            <ul class="space-y-3 text-gray-600 text-sm">
              <li>✔ Custom-built systems (no templates)</li>
              <li>✔ Scalable SaaS-ready architecture</li>
              <li>✔ Clean UI/UX with performance focus</li>
              <li>✔ CMS included for content control</li>
            </ul>
          </div>

          <div>
            <h3 class="font-semibold mb-2">Contact Info</h3>
            <p class="text-gray-500 text-sm">info@fixkraftdigital.com</p>
            <p class="text-gray-500 text-sm">+254 7XX XXX XXX</p>
          </div>

          <div class="p-4 bg-gray-50 rounded-xl text-sm text-gray-600">
            ⚡ Average response time: <span class="font-semibold">under 24 hours</span>
          </div>

        </div>

        <!-- RIGHT: FORM -->
        <div data-aos="fade-left">

          <form
            @submit.prevent="submitForm"
            class="bg-white shadow-xl rounded-2xl p-8 space-y-5 border"
          >

            <h2 class="text-xl font-semibold mb-2">
              Start Your Project
            </h2>

            <!-- NAME -->
            <!-- <input
              v-model="form.name"
              type="text"
              placeholder="Your Name"
              required
              class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary outline-none"
            /> -->

            <BaseInput v-model="form.name" placeholder="Your Name" required type="text" />

            <!-- EMAIL -->
            <!-- <input
              v-model="form.email"
              type="email"
              placeholder="Your Email"
              required
              class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary outline-none"
            /> -->

            <BaseInput v-model="form.email" type="email" placeholder="Your Email" required />

            <!-- SERVICE -->
            <select
              v-model="form.service"
              required
              class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary outline-none"
            >
              <option value="">Select Service</option>
              <option>Website Development</option>
              <option>SaaS Dashboard</option>
              <option>Custom CMS</option>
              <option>Branding</option>
            </select>

            <!-- BUDGET -->
            <select
              v-model="form.budget"
              class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary outline-none"
            >
              <option value="">Project Budget (Optional)</option>
              <option>$100 - $500</option>
              <option>$500 - $2000</option>
              <option>$2000+</option>
            </select>

            <!-- MESSAGE -->
            <textarea
              v-model="form.message"
              rows="4"
              placeholder="Tell us about your project..."
              class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary outline-none"
            ></textarea>

            <!-- BUTTON -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:scale-105 transition disabled:opacity-50"
            >
              {{ loading ? 'Sending...' : 'Start Project 🚀' }}
            </button>

            <!-- SUCCESS -->
            <p v-if="success" class="text-green-600 text-sm text-center">
              ✅ Message sent successfully!
            </p>

          </form>

        </div>

      </div>
    </section>

  </div>
</template>