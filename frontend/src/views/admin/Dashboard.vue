<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import VisitorsChart from '@/components/dashboard/VisitorsChart.vue'
import ServicesChart from '@/components/dashboard/ServicesChart.vue'
import { onMounted, ref, computed, watch } from 'vue'
import axios from 'axios'
import { API_BASE_URI } from '@/config/api'
import { useAuthStore } from '@/stores/auth'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

const auth = useAuthStore()
const loading = ref(true)
const dashboardData = ref({
  stats: {
    projects: 0,
    inquiries: 0,
    clients: 0,
    quotations: 0,
    pending_quotations: 0,
    payments: 0
  },
  visitors: [] as number[],
  service_labels: [] as string[],
  top_clients: [] as any[],
  recent_quotations: [] as any[],
  service_data: [] as number[],
  recent_projects: [] as any[],
  activities: [] as { message: string; created_at: string }[]
})

const statsCards = computed(() => [
  { title: 'Projects', value: dashboardData.value.stats.projects, icon: '🚀', color: 'from-blue-500 to-cyan-500' },
  { title: 'Inquiries', value: dashboardData.value.stats.inquiries, icon: '📩', color: 'from-purple-500 to-pink-500' },
  { title: 'Clients', value: dashboardData.value.stats.clients, icon: '👥', color: 'from-green-500 to-emerald-500' },
  { title: 'Quotations', value: dashboardData.value.stats.quotations, icon: '📄', color: 'from-orange-500 to-red-500' },
  { title: 'Pending Quotations', value: dashboardData.value.stats.pending_quotations, icon: '⏳', color: 'from-yellow-500 to-amber-500' },
  { title: 'Payments', value: dashboardData.value.stats.payments, icon: '💰', color: 'from-teal-500 to-cyan-500' }
])

// Count-up animation: numbers will transition smoothly
// Create a separate ref for animated values and watch the real values
const animatedStats = ref({ ...dashboardData.value.stats })
watch(() => dashboardData.value.stats, (newStats) => {
  // Animate each stat from current to new value
  for (const key in newStats) {
    const target = newStats[key as keyof typeof animatedStats.value]
    const start = animatedStats.value[key as keyof typeof animatedStats.value]
    if (start === target) continue
    const duration = 500
    const step = (target - start) / (duration / 16)
    let current = start
    const interval = setInterval(() => {
      current += step
      if ((step > 0 && current >= target) || (step < 0 && current <= target)) {
        animatedStats.value[key as keyof typeof animatedStats.value] = target
        clearInterval(interval)
      } else {
        animatedStats.value[key as keyof typeof animatedStats.value] = Math.floor(current)
      }
    }, 16);
  }
}, { deep: true })

// Date and time greeting
const greeting = computed(() => {
  const hour = new Date().getHours()
  let timeOfDay = 'morning'
  if (hour >= 12 && hour < 18) timeOfDay = 'afternoon'
  if (hour >= 18) timeOfDay = 'evening'
  const userName = auth.user?.username || 'Admin'
  const today = dayjs().format('dddd, MMMM D, YYYY')
  return `Good ${timeOfDay}, ${userName}. Today is ${today}.`
})

const formatRelativeTime = (isoString: string) => {
  return dayjs(isoString).fromNow()
}

// fetch visitors trend
const visitorTrend = ref(0)

const fetchDashboardData = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE_URI}/dashboard/stats/`)
    dashboardData.value = res.data
    visitorTrend.value = res.data.visitor_trend
  } catch (error) {
    console.error('Failed to fetch dashboard stats', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await auth.fetchCurrentUser()
  fetchDashboardData()
})

</script>

<template>
  <div class="space-y-8">
    <!-- HEADER with refresh button -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-text">Dashboard</h1>
        <p class="text-text/60 mt-1">{{ greeting }}</p>
      </div>
      
      <!-- Base button with refresh button -->
       <div class="flex items-center gap-3">
        <BaseButton>+ New Project</BaseButton>
        <button @click="fetchDashboardData" class="p-2 rounded-full hover:bg-gray-100 transition" title="Refresh Dashboard">
        🔄
      </button>
       </div>
    </div>

    <!-- HERO (unchanged) -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary to-secondary p-10 text-white">
      <div class="relative z-10 max-w-2xl">
        <p class="uppercase text-sm tracking-widest opacity-80 mb-3">Admin Overview</p>
        <h2 class="text-4xl font-bold leading-tight mb-4">Manage your digital platform professionally.</h2>
        <p class="text-white/80">Track projects, services, messages, and website content from one place.</p>
      </div>
      <div class="absolute -right-20 -top-20 w-72 h-72 bg-white/10 rounded-full blur-3xl" />
    </div>

    <!-- STATS CARDS with animated numbers -->
    <div class="grid md:grid-cols-3 lg:grid-cols-6 gap-6">
      <div v-for="stat in statsCards" :key="stat.title" class="group relative overflow-hidden rounded-2xl bg-white p-6 shadow-sm hover:shadow-xl transition duration-300">
        <div class="flex items-center justify-between mb-6">
          <div>
            <p class="text-sm text-gray-500">{{ stat.title }}</p>
            <h2 class="text-3xl font-bold mt-2">
              {{ animatedStats[stat.title.toLowerCase() as keyof typeof animatedStats] }}
            </h2>
          </div>
          <div class="h-14 w-14 rounded-2xl flex items-center justify-center text-2xl bg-gradient-to-br text-white" :class="stat.color">
            {{ stat.icon }}
          </div>
        </div>
        <div class="absolute bottom-0 left-0 h-1 w-full bg-gradient-to-r opacity-0 group-hover:opacity-100 transition" :class="stat.color" />
      </div>
    </div>

    <!-- ANALYTICS CHARTS -->
    <div class="grid lg:grid-cols-3 gap-6">
      <BaseCard class="lg:col-span-2">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-xl font-semibold">Website Analytics</h2>
            <p class="text-sm text-gray-500">Weekly visitor performance</p>
          </div>
          <div class="text-sm font-medium" :class="visitorTrend >= 0 ? 'text-green-500' : 'text-red-500'">
            {{ visitorTrend >= 0 ? '+' : '' }}{{ visitorTrend }}
          </div>
        </div>
        <VisitorsChart :data="dashboardData.visitors" :loading="loading" />
      </BaseCard>

      <BaseCard>
        <div class="mb-6">
          <h2 class="text-xl font-semibold">Services Distribution</h2>
          <p class="text-sm text-gray-500">Most requested services</p>
        </div>
        <ServicesChart :labels="dashboardData.service_labels" :data="dashboardData.service_data" :loading="loading" />
      </BaseCard>
    </div>

    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Basecard for top clients -->
      <BaseCard>
        <h2 class="text-xl font-semibold mb-4">Top Clients</h2>
        <div class="space-y-3">
          <div v-for="client in dashboardData.top_clients" :key="client.name" class="flex justify-between items-center border-b pb-2">
            <span class="text-sm font-medium">{{ client.name }}</span>
            <span class="text-sm text-gray-500">{{ client.count }} inquiries</span>
          </div>
          <div v-if="dashboardData.top_clients.length === 0 && !loading" class="text-center text-gray-500 py-4">
            No clients yet
          </div>
        </div>
      </BaseCard>

      <!-- Recent Quotations -->
      <BaseCard>
        <h2 class="text-xl font-semibold mb-4">Recent Quotations</h2>
        <div class="space-y-3">
          <div v-for="q in dashboardData.recent_quotations" :key="q.number" class="flex justify-between items-center border-b pb-2">
            <div class="">
              <p class="text-sm font-medium">{{ q.client }}</p>
              <p class="text-xs text-gray-500">{{ q.number }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold">KSh {{ q.amount.toLocaleString() }}</p>
              <p class="text-sm" :class="{'text-yellow-600': q.status === 'pending', 'text-green-600': q.status === 'approved'}">
                {{ q.status }}
              </p>
            </div>
          </div>
          <div v-if="dashboardData.recent_quotations.length === 0 && !loading" class="text-center text-gray-500 py-4">
            No quotations yet
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- QUICK ACTIONS (unchanged) -->
    <BaseCard>
      <div class="flex items-center justify-between mb-6"><h2 class="text-xl font-semibold">Quick Actions</h2><p class="text-sm text-gray-500">Manage content faster</p></div>
      <div class="grid md:grid-cols-4 gap-4">
        <router-link to="/admin/projects" class="p-5 rounded-2xl border hover:border-primary hover:shadow-md transition group">
          <div class="text-3xl mb-3">🚀</div><h3 class="font-semibold group-hover:text-primary transition">Projects</h3><p class="text-sm text-gray-500 mt-1">Manage portfolio work</p>
        </router-link>
        <router-link to="/admin/inquiries" class="p-5 rounded-2xl border hover:border-primary hover:shadow-md transition group">
          <div class="text-3xl mb-3">📩</div><h3 class="font-semibold group-hover:text-primary transition">Inquiries</h3><p class="text-sm text-gray-500 mt-1">View client inquiries</p>
        </router-link>
        <router-link to="/admin/quotations" class="p-5 rounded-2xl border hover:border-primary hover:shadow-md transition group">
          <div class="text-3xl mb-3">📄</div><h3 class="font-semibold group-hover:text-primary transition">Quotations</h3><p class="text-sm text-gray-500 mt-1">Manage quotes</p>
        </router-link>
        <router-link to="/admin/settings" class="p-5 rounded-2xl border hover:border-primary hover:shadow-md transition group">
          <div class="text-3xl mb-3">⚙️</div><h3 class="font-semibold group-hover:text-primary transition">Settings</h3><p class="text-sm text-gray-500 mt-1">Customize platform</p>
        </router-link>
      </div>
    </BaseCard>

    <!-- RECENT PROJECTS & ACTIVITY -->
    <div class="grid lg:grid-cols-3 gap-6">
      <BaseCard class="lg:col-span-2">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold">Recent Projects</h2>
          <router-link to="/admin/projects" class="text-primary text-sm">View all</router-link>
        </div>
        <div class="space-y-4">
          <div v-for="project in dashboardData.recent_projects" :key="project.id" class="flex items-center justify-between p-4 rounded-xl border hover:bg-gray-50 transition">
            <div><h3 class="font-medium">{{ project.title }}</h3><p class="text-sm text-gray-500">Recently updated</p></div><div class="text-xl">→</div>
          </div>
          <div v-if="dashboardData.recent_projects.length === 0 && !loading" class="text-center text-gray-500 py-4">No recent projects</div>
        </div>
      </BaseCard>

      <BaseCard>
        <h2 class="text-xl font-semibold mb-6">Activity</h2>
        <div class="space-y-5">
          <div v-for="activity in dashboardData.activities" :key="activity.message" class="flex gap-3">
            <div class="w-3 h-3 rounded-full bg-primary mt-2" />
              <div>
                <p class="text-sm font-medium">{{ activity.message }}</p>
                <p class="text-xs text-gray-500">{{ formatRelativeTime(activity.created_at) }}</p>
              </div>
          </div>
          <div v-if="dashboardData.activities.length === 0 && !loading" class="text-center text-gray-500 py-4">No recent activity</div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>