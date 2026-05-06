<script setup lang="ts">
import { ref } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useSiteConfig } from '@/stores/siteConfig'

const theme = useThemeStore()

const activeTab = ref('appearance')

// HANDLERS
const toggleDark = () => theme.toggleDark()

const updatePrimary = (e: Event) => {
  const color = (e.target as HTMLInputElement).value
  theme.setPrimary(color)
}

// site name save
const siteName = ref('FixKraft Digital')
const email = ref('info@foxkraftdigital.com')

const saveGeneral = () => {
    config.saveGeneral()

    alert('General Settings saved!')
}

const logo = ref<string | null>(localStorage.getItem('logo'))

// appearance tab
const config = useSiteConfig()

const uploadLogo = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0]

    if (!file) return

    const reader = new FileReader()
    reader.onload = () => {
        config.logo = reader.result as string
    }
    reader.readAsDataURL(file)
}

const saveBranding = () => {
    config.saveBranding()
    alert('Branding Saved!')
}

const addLink = () => {
    config.navLinks.push({ name: '', path: '' })
}

const removeLink = (i: number) => {
    config.navLinks.splice(i, 1)
}

const saveNav = () => {
    config.saveNav()
    alert('NAvifation saved!')
}

// Footer Tab
const saveFooter = () => {
    config.saveFooter()
    alert('Footer saved!')
}

</script>

<template>
  <div class="flex gap-8">

    <!-- LEFT SIDEBAR -->
    <aside class="w-56">

      <nav class="space-y-1">

        <button
          v-for="tab in ['appearance', 'general', 'navigation', 'footer', 'billing']"
          :key="tab"
          @click="activeTab = tab"
          class="w-full text-left px-3 py-2 rounded-lg text-sm capitalize transition"
          :class="activeTab === tab
            ? 'bg-primary/10 text-primary font-medium'
            : 'text-text/70 hover:bg-gray-100'"
        >
          {{ tab }}
        </button>

      </nav>

    </aside>

    <!-- RIGHT CONTENT -->
    <div class="flex-1 max-w-3xl">

      <!-- APPEARANCE -->
      <div v-if="activeTab === 'appearance'">

        <div class="mb-8">
          <h1 class="text-xl font-semibold text-text">
            Appearance
          </h1>
          <p class="text-sm text-text/60">
            Customize how your platform looks
          </p>
        </div>

        <div class="bg-surface border border-border rounded-xl divide-y divide-border">

          <!-- DARK MODE -->
          <div class="flex items-center justify-between px-6 py-4">
            <div>
              <p class="text-sm font-medium text-text">Dark mode</p>
              <p class="text-xs text-text/60">Switch UI theme</p>
            </div>

            <button
              @click="toggleDark"
              class="relative inline-flex h-6 w-11 items-center rounded-full transition"
              :class="theme.dark ? 'bg-primary' : 'bg-gray-300'"
            >
              <span
                class="inline-block h-4 w-4 transform rounded-full bg-white transition"
                :class="theme.dark ? 'translate-x-6' : 'translate-x-1'"
              />
            </button>
          </div>

          <!-- PRIMARY COLOR -->
          <div class="flex items-center justify-between px-6 py-4">
            <div>
              <p class="text-sm font-medium text-text">Brand color</p>
              <p class="text-xs text-text/60">Used across UI</p>
            </div>

            <input
              type="color"
              :value="theme.primary"
              @input="updatePrimary"
              class="h-10 w-16 border border-border rounded-md cursor-pointer"
            />
          </div>

          <!-- LOGO UPLOAD -->
            <div class="flex items-center justify-between px-6 py-4">
                <div>
                    <p class="text-sm font-medium text-text">Logo</p>
                    <p class="text-xs text-text/60">Upload brand logo</p>
                </div>

                <input type="file" accept="image/*" @change="uploadLogo" />
                </div>

                <!-- PREVIEW -->
                <div v-if="logo" class="px-6 py-4">
                <img :src="logo" class="h-12 object-contain" />
            </div>
            <div class="px-6 py-4 flex justify-end">
                <button @click="saveBranding" class="bg-primary text-white px-5 py-2 rounded-lg">
                    Save Branding
                </button>
            </div>

        </div>

      </div>

      <!-- GENERAL -->
      <div v-if="activeTab === 'general'">

        <div class="mb-8">
          <h1 class="text-xl font-semibold text-text">
            General
          </h1>
          <p class="text-sm text-text/60">
            Basic platform information
          </p>
        </div>

        <div class="bg-surface border border-border rounded-xl divide-y divide-border">

          <!-- SITE NAME -->
          <div class="px-6 py-4 space-y-2">
            <p class="text-sm font-medium text-text">Site name</p>
            <input
            v-model="config.siteName"
              type="text"
              placeholder="FixKraft Digital"
              class="w-full px-3 py-2 border border-border rounded-md bg-transparent text-text outline-none focus:ring-2 focus:ring-primary/30"
            />
          </div>

          <!-- EMAIL -->
          <div class="px-6 py-4 space-y-2">
            <p class="text-sm font-medium text-text">Contact email</p>
            <input
            v-model="config.email"
              type="email"
              placeholder="info@fixkraft.com"
              class="w-full px-3 py-2 border border-border rounded-md bg-transparent text-text outline-none focus:ring-2 focus:ring-primary/30"
            />
          </div>

          <div class="px-6 py-4 flex justify-end">
            <button
                @click="saveGeneral"
                class="bg-primary text-white px-5 py-2 rounded-lg hover:opacity-90"
            >
                Save Changes
            </button>
          </div>

        </div>

      </div>

      <!-- FOOTER -->
<div v-if="activeTab === 'footer'">

  <div class="mb-8">
    <h1 class="text-xl font-semibold text-text">Footer</h1>
    <p class="text-sm text-text/60">
      Manage footer content
    </p>
  </div>

  <div class="bg-surface border border-border rounded-xl p-6 space-y-4">

    <div>
      <p class="text-sm mb-1">Phone</p>
      <input
        v-model="config.phone"
        class="w-full px-3 py-2 border border-border rounded-md"
      />
    </div>

    <div>
      <p class="text-sm mb-1">Location</p>
      <input
        v-model="config.location"
        class="w-full px-3 py-2 border border-border rounded-md"
      />
    </div>

    <div class="flex justify-end">
      <button
        @click="saveFooter"
        class="bg-primary text-white px-5 py-2 rounded-lg"
      >
        Save Footer
      </button>
    </div>

  </div>
</div>
      <!-- NAVIGATION -->
        <div v-if="activeTab === 'navigation'">

        <div class="mb-8">
            <h1 class="text-xl font-semibold text-text">Navigation</h1>
            <p class="text-sm text-text/60">
            Manage navbar links
            </p>
        </div>

        <div class="bg-surface border border-border rounded-xl p-6 space-y-4">

            <div
            v-for="(link, i) in config.navLinks"
            :key="i"
            class="flex gap-2 items-center"
            >
            <input
                v-model="link.name"
                placeholder="Name"
                class="flex-1 px-3 py-2 border border-border rounded-md"
            />

            <input
                v-model="link.path"
                placeholder="/path"
                class="flex-1 px-3 py-2 border border-border rounded-md"
            />

            <button
                @click="removeLink(i)"
                class="text-red-500 hover:scale-110"
            >
                ❌
            </button>
            </div>

            <button
            @click="addLink"
            class="text-sm text-primary"
            >
            + Add Link
            </button>

            <div class="flex justify-end">
            <button
                @click="saveNav"
                class="bg-primary text-white px-5 py-2 rounded-lg"
            >
                Save Navigation
            </button>
            </div>

        </div>
        </div>

      <!-- BILLING -->
      <div v-if="activeTab === 'billing'">

        <div class="mb-8">
          <h1 class="text-xl font-semibold text-text">
            Billing
          </h1>
          <p class="text-sm text-text/60">
            Manage subscription and payments
          </p>
        </div>

        <div class="bg-surface border border-border rounded-xl p-6 space-y-4">

          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-text">Current Plan</p>
              <p class="text-xs text-text/60">Pro Plan</p>
            </div>

            <button class="text-sm text-primary hover:underline">
              Upgrade
            </button>
          </div>

          <div class="border-t border-border pt-4">
            <p class="text-sm text-text/60">
              Billing integration (Stripe) will go here later.
            </p>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>