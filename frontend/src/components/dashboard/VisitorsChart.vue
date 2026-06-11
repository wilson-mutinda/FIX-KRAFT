<script setup lang="ts">
import { computed } from 'vue'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler } from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler)

const props = defineProps<{
  data?: number[]
  loading?: boolean
}>()

const chartData = computed(() => ({
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  datasets: [{
    label: 'Visitors',
    data: props.data?.length ? props.data : [0, 0, 0, 0, 0, 0, 0],
    fill: true,
    tension: 0.4,
    backgroundColor: 'rgba(99,102,241,0.15)',
    borderColor: '#6366f1',
    pointBackgroundColor: '#6366f1'
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }
}
</script>

<template>
  <div class="h-[320px]">
    <Line v-if="!loading" :data="chartData" :options="chartOptions" />
    <div v-else class="h-full flex items-center justify-center text-gray-400">Loading chart...</div>
  </div>
</template>