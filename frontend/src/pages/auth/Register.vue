<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const auth = useAuthStore()
const router = useRouter()

const first_name = ref('')
const last_name = ref('')
const email = ref('')
const password = ref('')

const loading = ref(false)
const errorMessage = ref('')

const handleRegister = async () => {

  loading.value = true
  errorMessage.value = ''

  const response = await auth.register({
    first_name: first_name.value,
    last_name: last_name.value,
    email: email.value,
    password: password.value
  })

  loading.value = false

  if (response.success) {

    router.push('/login')

  } else {

    errorMessage.value = 'Registration failed'

  }
}
</script>

<template>
  <div class="min-h-screen relative overflow-hidden bg-secondary/5">

    <!-- BACKGROUND BLURS -->
    <div
      class="absolute top-[-120px] left-[-120px] h-72 w-72 rounded-full bg-primary/20 blur-3xl"
    />

    <div
      class="absolute bottom-[-120px] right-[-120px] h-72 w-72 rounded-full bg-secondary/20 blur-3xl"
    />

    <!-- CONTENT -->
    <div class="relative z-10 min-h-screen grid lg:grid-cols-2">

      <!-- LEFT SIDE -->
      <div
        class="hidden lg:flex flex-col justify-between bg-secondary text-white p-12"
      >

        <!-- BRAND -->
        <div>

          <div
            class="h-36 w-36 rounded-2xl bg-primar flex items-center justify-center shadow-lg"
          >
            <img src="/fix-kraft-logo-blue-bg.svg" alt="">
          </div>

          <div class="mt-6">

            <h1 class="text-5xl font-extrabold tracking-tight leading-tight">
              Join
              <span class="text-primary">
                FixKraft
              </span>
            </h1>

            <p class="mt-5 text-lg text-white/70 max-w-md leading-relaxed">
              Build modern digital experiences,
              scalable systems, and premium software solutions.
            </p>

          </div>

        </div>

        <!-- FEATURES -->
        <div class="space-y-5">

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Modern Dashboard Experience</span>
          </div>

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Fast & Secure Authentication</span>
          </div>

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Client & Project Management</span>
          </div>

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Scalable SaaS Infrastructure</span>
          </div>

        </div>

      </div>

      <!-- RIGHT SIDE -->
      <div class="flex items-center justify-center p-6 lg:p-12">

        <div
          class="w-full max-w-md bg-surface/90 backdrop-blur-xl border border-border rounded-3xl shadow-2xl p-8 lg:p-10"
        >

          <!-- MOBILE LOGO -->
          <div class="lg:hidden flex justify-center mb-6">

            <div
              class="h-36 w-36 rounded-2xl bg-primar flex items-center justify-center shadow-lg"
            >
              <img src="/fix-kraft-logo-no-bg.svg" alt="">
            </div>

          </div>

          <!-- HEADER -->
          <div class="text-center">

            <h2 class="text-4xl font-extrabold tracking-tight text-text">
              Create Account
            </h2>

            <p class="mt-3 text-text/70">
              Start your FixKraft Digital journey
            </p>

          </div>

          <!-- FORM -->
          <form
            @submit.prevent="handleRegister"
            class="mt-10 space-y-5"
          >

            <!-- FIRST NAME -->
            <div>

              <label class="block mb-2 text-sm font-medium text-text">
                First Name
              </label>

              <BaseInput
                v-model="first_name"
                type="text"
                placeholder="Enter first name"
              />

            </div>

            <!-- LAST NAME -->
            <div>

              <label class="block mb-2 text-sm font-medium text-text">
                Last Name
              </label>

              <BaseInput
                v-model="last_name"
                type="text"
                placeholder="Enter last name"
              />

            </div>

            <!-- EMAIL -->
            <div>

              <label class="block mb-2 text-sm font-medium text-text">
                Email Address
              </label>

              <BaseInput
                v-model="email"
                type="email"
                placeholder="Enter your email"
              />

            </div>

            <!-- PASSWORD -->
            <div>

              <label class="block mb-2 text-sm font-medium text-text">
                Password
              </label>

              <BaseInput
                v-model="password"
                type="password"
                placeholder="Create password"
              />

            </div>

            <!-- ERROR -->
            <div
              v-if="errorMessage"
              class="bg-red-100 border border-red-200 text-red-600 text-sm p-4 rounded-xl"
            >
              {{ errorMessage }}
            </div>

            <!-- BUTTON -->
            <BaseButton
              type="submit"
              class="w-full"
              :disabled="loading"
            >

              <span v-if="loading" class="animate-spin">
                Creating Account...
              </span>

              <span v-else>
                Register
              </span>

            </BaseButton>

          </form>

          <!-- FOOTER -->
          <div class="mt-8 text-center text-sm text-text/70">

            Already have an account?

            <button
              @click="router.push('/login')"
              class="text-primary font-semibold hover:underline ml-1"
            >
              Login
            </button>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>