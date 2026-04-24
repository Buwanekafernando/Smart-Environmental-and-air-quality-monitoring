<template>
  <div class="humidity-card">
    <div class="card-header">
      <h2>💧 Humidity</h2>
      <div class="current-val" v-if="latestHumidity > 0">
        {{ latestHumidity.toFixed(1) }}%
      </div>
    </div>
    <div class="chart-container">
      <!-- :key forces vue-chartjs to fully re-render when data reference changes -->
      <Line :key="chartKey" :data="computedChartData" :options="chartOptions"/>
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

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend, Filler)

export default {
  name: "HumidityChart",
  components: { Line },
  props: {
    humidityTrend:  { type: Array,  default: () => [] },
    labels:         { type: Array,  default: () => [] },
    latestHumidity: { type: Number, default: 0 },
    chartKey:       { type: Number, default: 0 }
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [{
          label: "Humidity (%)",
          data: [],
          borderColor: "#0ea5e9",
          borderWidth: 3,
          pointRadius: 0,
          pointHoverRadius: 4,
          tension: 0.2,
          fill: true,
          backgroundColor: (context) => {
            const chart = context.chart;
            const { ctx, chartArea } = chart;
            if (!chartArea) return null;
            const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            gradient.addColorStop(0, "rgba(14, 165, 233, 0.2)");
            gradient.addColorStop(1, "rgba(14, 165, 233, 0)");
            return gradient;
          }
        }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            suggestedMin: 30,
            suggestedMax: 80,
            grid: { color: "#f1f5f9" },
            ticks: { 
              font: { size: 10, weight: '600' },
              color: '#94a3b8',
              callback: (value) => value + '%'
            }
          },
          x: {
            display: true,
            title: {
              display: true,
              color: '#94a3b8',
              font: { size: 10, weight: 'bold' }
            },
            grid: { display: false },
            ticks: { 
              font: { size: 10, weight: '600' },
              color: '#94a3b8',
              maxRotation: 0,
              autoSkip: true,
              maxTicksLimit: 10
            }
          }
        }
      }
    }
  },
  computed: {
    computedChartData() {
      return {
        labels: this.labels,
        datasets: [{
          ...this.chartData.datasets[0],
          data: this.humidityTrend
        }]
      };
    }
  }
}
</script>

<style scoped>
.humidity-card {
  background: white;
  padding: 18px;
  border-radius: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

h2 {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  color: #334155;
}

.current-val {
  font-size: 1.1rem;
  font-weight: 800;
  color: #0ea5e9;
}

.chart-container {
  flex: 1;
  min-height: 0;
}
</style>
