<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import VisitorsChart from '@/components/dashboard/VisitorsChart.vue'
import ServicesChart from '@/components/dashboard/ServicesChart.vue'

const stats = [
  {
    title: 'Projects',
    value: 12,
    icon: '🚀',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    title: 'Messages',
    value: 5,
    icon: '📩',
    color: 'from-purple-500 to-pink-500'
  },
  {
    title: 'Services',
    value: 4,
    icon: '🛠️',
    color: 'from-orange-500 to-red-500'
  },
  {
    title: 'Visitors',
    value: '1.2k',
    icon: '📈',
    color: 'from-green-500 to-emerald-500'
  }
]

const recentProjects = [
  'SaaS Dashboard',
  'School CMS',
  'Portfolio Website'
]

const activities = [
  'Added new service',
  'Updated homepage',
  'Uploaded project image',
  'Changed logo'
]
</script>

<template>
  <div class="space-y-8">

    <!-- HEADER -->
    <div class="flex items-center justify-between">

      <div>
        <h1 class="text-3xl font-bold text-text">
          Dashboard
        </h1>

        <p class="text-text/60 mt-1">
          Welcome back, Wilson 👋
        </p>
      </div>

      <BaseButton>
        + New Project
      </BaseButton>

    </div>

    <!-- HERO -->
    <div
      class="relative overflow-hidden rounded-3xl
             bg-gradient-to-br from-primary to-secondary
             p-10 text-white"
    >

      <div class="relative z-10 max-w-2xl">

        <p class="uppercase text-sm tracking-widest opacity-80 mb-3">
          Admin Overview
        </p>

        <h2 class="text-4xl font-bold leading-tight mb-4">
          Manage your digital platform professionally.
        </h2>

        <p class="text-white/80">
          Track projects, services, messages, and website content from one place.
        </p>

      </div>

      <!-- BACKGROUND GLOW -->
      <div
        class="absolute -right-20 -top-20 w-72 h-72
               bg-white/10 rounded-full blur-3xl"
      />

    </div>

    <!-- STATS -->
    <div class="grid md:grid-cols-4 gap-6">

      <div
        v-for="stat in stats"
        :key="stat.title"
        class="group relative overflow-hidden rounded-2xl
               bg-white p-6 shadow-sm hover:shadow-xl
               transition duration-300"
      >

        <!-- TOP -->
        <div class="flex items-center justify-between mb-6">

          <div>
            <p class="text-sm text-gray-500">
              {{ stat.title }}
            </p>

            <h2 class="text-3xl font-bold mt-2">
              {{ stat.value }}
            </h2>
          </div>

          <div
            class="h-14 w-14 rounded-2xl flex items-center justify-center text-2xl
                   bg-gradient-to-br text-white"
            :class="stat.color"
          >
            {{ stat.icon }}
          </div>

        </div>

        <!-- GLOW -->
        <div
          class="absolute bottom-0 left-0 h-1 w-full
                 bg-gradient-to-r opacity-0 group-hover:opacity-100
                 transition"
          :class="stat.color"
        />

      </div>

    </div>

    <!-- ANALYTICS -->
    <div class="grid lg:grid-cols-3 gap-6">

      <!-- VISITORS -->
      <BaseCard class="lg:col-span-2">

        <div class="flex items-center justify-between mb-6">

          <div>
            <h2 class="text-xl font-semibold">
              Website Analytics
            </h2>

            <p class="text-sm text-gray-500">
              Weekly visitor performance
            </p>
          </div>

          <div class="text-sm text-green-500 font-medium">
            +18%
          </div>

        </div>

        <VisitorsChart />

      </BaseCard>

      <!-- PIE -->
      <BaseCard>

        <div class="mb-6">

          <h2 class="text-xl font-semibold">
            Services Distribution
          </h2>

          <p class="text-sm text-gray-500">
            Most requested services
          </p>

        </div>

        <ServicesChart />

      </BaseCard>

    </div>

    <!-- QUICK ACTIONS -->
    <BaseCard>

      <div class="flex items-center justify-between mb-6">

        <h2 class="text-xl font-semibold">
          Quick Actions
        </h2>

        <p class="text-sm text-gray-500">
          Manage content faster
        </p>

      </div>

      <div class="grid md:grid-cols-4 gap-4">

        <router-link
          to="/admin/projects"
          class="p-5 rounded-2xl border hover:border-primary
                 hover:shadow-md transition group"
        >
          <div class="text-3xl mb-3">🚀</div>

          <h3 class="font-semibold group-hover:text-primary transition">
            Projects
          </h3>

          <p class="text-sm text-gray-500 mt-1">
            Manage portfolio work
          </p>
        </router-link>

        <router-link
          to="/admin/services"
          class="p-5 rounded-2xl border hover:border-primary
                 hover:shadow-md transition group"
        >
          <div class="text-3xl mb-3">🛠️</div>

          <h3 class="font-semibold group-hover:text-primary transition">
            Services
          </h3>

          <p class="text-sm text-gray-500 mt-1">
            Edit service offerings
          </p>
        </router-link>

        <router-link
          to="/admin/messages"
          class="p-5 rounded-2xl border hover:border-primary
                 hover:shadow-md transition group"
        >
          <div class="text-3xl mb-3">📩</div>

          <h3 class="font-semibold group-hover:text-primary transition">
            Messages
          </h3>

          <p class="text-sm text-gray-500 mt-1">
            View client inquiries
          </p>
        </router-link>

        <router-link
          to="/admin/settings"
          class="p-5 rounded-2xl border hover:border-primary
                 hover:shadow-md transition group"
        >
          <div class="text-3xl mb-3">⚙️</div>

          <h3 class="font-semibold group-hover:text-primary transition">
            Settings
          </h3>

          <p class="text-sm text-gray-500 mt-1">
            Customize platform
          </p>
        </router-link>

      </div>

    </BaseCard>

    <!-- LOWER GRID -->
    <div class="grid lg:grid-cols-3 gap-6">

      <!-- RECENT PROJECTS -->
      <BaseCard class="lg:col-span-2">

        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold">
            Recent Projects
          </h2>

          <router-link
            to="/admin/projects"
            class="text-primary text-sm"
          >
            View all
          </router-link>
        </div>

        <div class="space-y-4">

          <div
            v-for="project in recentProjects"
            :key="project"
            class="flex items-center justify-between p-4
                   rounded-xl border hover:bg-gray-50 transition"
          >

            <div>
              <h3 class="font-medium">
                {{ project }}
              </h3>

              <p class="text-sm text-gray-500">
                Recently updated
              </p>
            </div>

            <div class="text-xl">
              →
            </div>

          </div>

        </div>

      </BaseCard>

      <!-- ACTIVITY -->
      <BaseCard>

        <h2 class="text-xl font-semibold mb-6">
          Activity
        </h2>

        <div class="space-y-5">

          <div
            v-for="activity in activities"
            :key="activity"
            class="flex gap-3"
          >

            <div class="w-3 h-3 rounded-full bg-primary mt-2" />

            <div>
              <p class="text-sm font-medium">
                {{ activity }}
              </p>

              <p class="text-xs text-gray-500">
                Just now
              </p>
            </div>

          </div>

        </div>

      </BaseCard>

    </div>

  </div>
</template>