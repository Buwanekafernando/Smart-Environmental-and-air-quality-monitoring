<template>
<div class="air-card">
  <div class="chart-section">
    <div class="chart-header">
      <h2>🌬 Air Quality Index</h2>
      <div class="aqi-badge" :style="{ backgroundColor: currentAqi ? currentAqi.color : '#888' }">
        {{ currentAqi && currentAqi.label ? currentAqi.label : 'Loading...' }}
      </div>
    </div>
    <div class="chart-wrapper">
      <Line :data="computedChartData" :options="chartOptions" />
    </div>
  </div>
  <div class="score-section">
    <div class="score-container">
      <h1 :style="{ color: currentAqi ? currentAqi.color : '#000' }">{{ currentAqi ? currentAqi.score : 0 }}</h1>
      <p>Current AQI</p>
    </div>
    <div class="aqi-bar-container">
      <div class="aqi-bar">
        <div class="aqi-fill" :style="{ backgroundColor: currentAqi ? currentAqi.color : '#ddd', width: Math.min(((currentAqi ? currentAqi.score : 0) / 5), 100) + '%' }"></div>
      </div>
      <div class="aqi-labels">
        <span>0</span>
        <span>500</span>
      </div>
    </div>
    <div v-if="trendsData" class="trend-box">
      <div class="trend-item">
        <span class="label">Trend:</span>
        <span class="value">{{ trendsData.trend }}</span>
      </div>
      <div class="trend-item">
        <span class="label">Forecast:</span>
        <span class="value">{{ trendsData.forecast }}</span>
      </div>
    </div>
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
  components: { Line },
  props: {
    aqiTrend: { type: Array, default: () => [] },
    currentAqi: { type: Object, default: () => ({}) },
    labels: { type: Array, default: () => [] },
    trendsData: { type: Object, default: null }
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [{
          label: "AQI",
          data: [],
          borderColor: "#3b82f6",
          pointRadius: 2,
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          backgroundColor: (context) => {
            const chart = context.chart;
            const { ctx, chartArea } = chart;
            if (!chartArea) return null;
            const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            gradient.addColorStop(0, "rgba(59, 130, 246, 0.2)");
            gradient.addColorStop(1, "rgba(59, 130, 246, 0)");
            return gradient;
          }
        }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            mode: 'index',
            intersect: false,
          }
        },
        scales: {
          y: {
            min: 0,
            max: 500,
            grid: { color: "#f1f5f9" },
            ticks: { font: { size: 10 } }
          },
          x: {
            grid: { display: false },
            ticks: { font: { size: 10 }, maxRotation: 0 }
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
          data: this.aqiTrend
        }]
      };
    }
  }
};
</script>

<style scoped>
.air-card {
  display: flex;
  background: #ffffff;
  padding: 20px;
  border-radius: 16px;
  height: 100%;
  gap: 20px;
}

.chart-section {
  flex: 2.5;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.chart-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  color: #334155;
}

.aqi-badge {
  padding: 4px 12px;
  border-radius: 20px;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.chart-wrapper {
  flex: 1;
  min-height: 0;
}

.score-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-left: 1px solid #f1f5f9;
  padding-left: 20px;
}

.score-container {
  text-align: center;
}

.score-container h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin: 0;
  line-height: 1;
}

.score-container p {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  margin: 5px 0 0 0;
}

.aqi-bar-container {
  margin: 15px 0;
}

.aqi-bar {
  width: 100%;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.aqi-fill {
  height: 100%;
  transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.aqi-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 0.65rem;
  font-weight: 600;
  color: #94a3b8;
}

.trend-box {
  background: #f8fafc;
  padding: 12px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.trend-item {
  display: flex;
  flex-direction: column;
}

.trend-item .label {
  font-size: 0.65rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.trend-item .value {
  font-size: 0.8rem;
  font-weight: 600;
  color: #334155;
  line-height: 1.2;
}
</style>