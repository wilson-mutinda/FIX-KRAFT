<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {

  loading.value = true
  errorMessage.value = ''

  const response = await auth.login(
    username.value,
    password.value
  )

  loading.value = false

  if (response.success) {

    router.push('/admin')

  } else {

    errorMessage.value = 'Invalid email or password'

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
        <div class="">

          <!-- LOGO -->
          <div
            class="h-36 w-36 rounded-2xl flex items-center justify-center text-2xl font-bold shadow-lg"
          >

            <img src="/fix-kraft-logo-blue-bg.svg" alt="">
          </div>

          <div class="mt-6">

            <h1 class="text-5xl font-extrabold tracking-tight leading-tight">
              FixKraft
              <span class="text-primary">
                Digital
              </span>
            </h1>

            <p class="mt-5 text-lg text-white/70 max-w-md leading-relaxed">
              Modern digital solutions, SaaS systems,
              branding, dashboards, and business automation.
            </p>

          </div>

        </div>

        <!-- FEATURES -->
        <div class="space-y-5">

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Secure Admin Dashboard</span>
          </div>

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Modern SaaS Architecture</span>
          </div>

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Projects & Client Management</span>
          </div>

          <div class="flex items-center gap-3 text-white/90">
            <span class="text-primary text-xl">✓</span>
            <span>Scalable Digital Solutions</span>
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
              Welcome Back
            </h2>

            <p class="mt-3 text-text/70">
              Login to continue to your dashboard
            </p>

          </div>

          <!-- FORM -->
          <form
            @submit.prevent="handleLogin"
            class="mt-10 space-y-6"
          >

            <!-- USERNAME -->
            <div>

              <label class="block mb-2 text-sm font-medium text-text">
                Username
              </label>

              <BaseInput
                v-model="username"
                type="username"
                placeholder="Enter your username"
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
                placeholder="Enter your password"
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

              <span v-if="loading">
                Logging in...
              </span>

              <span v-else>
                Login
              </span>

            </BaseButton>

          </form>

          <!-- FOOTER -->
          <div class="mt-8 text-center text-sm text-text/70">

            Don&apos;t have an account?

            <button
              @click="router.push('/register')"
              class="text-primary font-semibold hover:underline ml-1"
            >
              Register
            </button>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>