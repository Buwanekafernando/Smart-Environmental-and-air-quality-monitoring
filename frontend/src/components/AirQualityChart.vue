<template>
<div class="air-card">
  <div class="chart-section full-width">
    <div class="chart-header">
      <h2>🌬 Air Quality</h2>
      <div class="aqi-badge" :style="{ backgroundColor: currentAqi ? currentAqi.color : '#888' }">
        {{ currentAqi && currentAqi.label ? currentAqi.label : 'Loading...' }}
      </div>
    </div>
    <div class="chart-wrapper">
      <Line :data="computedChartData" :options="chartOptions" :plugins="visualZonesPlugin" />
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
      visualZonesPlugin: [{
        id: 'visualZones',
        beforeDraw: (chart) => {
          const { ctx, chartArea, scales: { y } } = chart;
          if (!chartArea) return;

          const drawZone = (min, max, color) => {
            const top = y.getPixelForValue(max);
            const bottom = y.getPixelForValue(min);
            ctx.save();
            ctx.fillStyle = color;
            ctx.fillRect(chartArea.left, top, chartArea.width, bottom - top);
            ctx.restore();
          };

          // Good (0-50)
          drawZone(0, 50, 'rgba(34, 197, 94, 0.1)');
          // Fair (51-100)
          drawZone(50, 100, 'rgba(234, 179, 8, 0.1)');
          // Poor (101-500)
          drawZone(100, 500, 'rgba(239, 68, 68, 0.1)');
        }
      }],
      chartData: {
        labels: [],
        datasets: [{
          label: "AQI",
          data: [],
          borderColor: "#1e293b",
          pointRadius: 0,
          borderWidth: 3,
          tension: 0.4,
          fill: false
        }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 }, // Faster updates
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
            grid: { color: "rgba(0,0,0,0.05)" },
            ticks: { font: { size: 10, weight: 'bold' } }
          },
          x: {
            grid: { display: false },
            ticks: { font: { size: 10, weight: 'bold' }, maxRotation: 0 }
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