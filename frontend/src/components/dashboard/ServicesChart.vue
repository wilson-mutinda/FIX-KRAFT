<script setup lang="ts">
import { computed } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  labels?: string[]
  data?: number[]
  loading?: boolean
}>()

const chartData = computed(() => ({
  labels: props.labels?.length ? props.labels : ['No data'],
  datasets: [{
    data: props.data?.length ? props.data : [1],
    backgroundColor: ['#6366f1', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444', '#06b6d4']
  }]
}))

const chartOptions = { responsive: true, maintainAspectRatio: false }
</script>

<template>
  <div class="h-[320px] flex items-center justify-center">
    <Pie v-if="!loading" :data="chartData" :options="chartOptions" />
    <div v-else class="text-gray-400">Loading chart...</div>
  </div>
</template>