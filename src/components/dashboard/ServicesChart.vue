<script setup lang="ts">
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

import { Pie } from 'vue-chartjs'

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
)

const chartData = {
  labels: [
    'Web',
    'CMS',
    'SaaS',
    'Branding'
  ],

  datasets: [
    {
      data: [40, 20, 30, 10],
      backgroundColor: [
        '#6366f1',
        '#8b5cf6',
        '#f59e0b',
        '#10b981'
      ]
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>

<template>
  <div class="h-[320px] flex items-center justify-center">
    <Pie
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>