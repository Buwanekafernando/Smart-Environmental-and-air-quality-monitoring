<template>
  <div class="air-card">
    <div class="chart-section">
      <h2>💧 Humidity Trend</h2>
      <Line :data="chartData" :options="chartOptions"/>
    </div>
  </div>
</template>

<script>
import { Line } from "vue-chartjs"
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler
} from "chart.js"

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler
)

export default {
  name: "HumidityChart",
  components: { Line },
  props: {
    humidityTrend: { type: Array, default: () => [] },
    labels: { type: Array, default: () => [] }
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [{
          label: "Humidity (%)",
          data: [],
          borderColor: "#0ea5e9", // Light blue
          pointRadius: 3,
          tension: 0.4,
          fill: true,
          backgroundColor: (context) => {
            const chart = context.chart
            const { ctx, chartArea } = chart
            if (!chartArea) return null
            const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom)
            gradient.addColorStop(0, "rgba(14, 165, 233, 0.5)")
            gradient.addColorStop(1, "rgba(14, 165, 233, 0.0)")
            return gradient
          }
        }]
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            min: 0,
            max: 100
          }
        }
      }
    }
  },
  watch: {
    humidityTrend: {
      handler(newVal) {
        this.chartData = {
          ...this.chartData,
          labels: this.labels,
          datasets: [{
            ...this.chartData.datasets[0],
            data: newVal
          }]
        };
      },
      deep: true,
      immediate: true
    }
  }
}
</script>

<style scoped>
.air-card {
  display: flex;
  background: #f3f3f3;
  padding: 30px;
  border-radius: 15px;
}
.chart-section {
  flex: 1;
}
</style>
