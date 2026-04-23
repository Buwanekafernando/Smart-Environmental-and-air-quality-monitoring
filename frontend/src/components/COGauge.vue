<template>
<div class="card">
  <div class="card-header">
    <h3>⚡ CO Level</h3>
    <div class="status-indicator" :class="statusClass">
      {{statusText}}
    </div>
  </div>
  
  <div class="gauge-section">
    <div class="gauge-container">
      <canvas ref="gaugeCanvas"></canvas>
    </div>
    <div class="value-display">
      <span class="value">{{coLevel}}</span>
      <span class="unit">%</span>
    </div>
  </div>
  
  <p class="description">CO Gas Amount in the Room</p>
</div>
</template>

<script>
import { Chart, ArcElement, Tooltip } from "chart.js"
Chart.register(ArcElement, Tooltip)

export default {
  props: {
    coLevel: { type: Number, default: 0 }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    coLevel() {
      if (this.chart) {
        this.updateGauge();
      }
    }
  },
  computed: {
    statusText() {
      if(this.coLevel < 40) return "Healthy"
      if(this.coLevel < 70) return "Warning"
      return "Danger"
    },
    statusClass() {
      if(this.coLevel < 40) return "low"
      if(this.coLevel < 70) return "medium"
      return "high"
    }
  },
  mounted() {
    this.createGauge()
  },
  methods: {
    createGauge() {
      const ctx = this.$refs.gaugeCanvas.getContext("2d")
      const needlePlugin = {
        id: "needle",
        afterDatasetDraw(chart) {
          const { ctx } = chart
          const needleValue = chart.config.data.datasets[0].needleValue || 0
          const clampedValue = Math.min(Math.max(needleValue, 0), 100)
          const angle = Math.PI + (clampedValue / 100) * Math.PI
          
          const cx = chart.getDatasetMeta(0).data[0].x
          const cy = chart.getDatasetMeta(0).data[0].y
          const outerRadius = chart.getDatasetMeta(0).data[0].outerRadius
          
          ctx.save()
          ctx.translate(cx, cy)
          ctx.rotate(angle)
          ctx.beginPath()
          ctx.moveTo(0, -2)
          ctx.lineTo(outerRadius - 10, 0) 
          ctx.lineTo(0, 2)
          ctx.fillStyle = "#1e293b"
          ctx.fill()
          ctx.restore()
          
          ctx.beginPath()
          ctx.arc(cx, cy, 6, 0, 2 * Math.PI)
          ctx.fillStyle = "#1e293b"
          ctx.fill()
        }
      }

      this.chart = new Chart(ctx, {
        type: "doughnut",
        data: {
          datasets: [{
            data: [40, 30, 30],
            backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
            borderWidth: 0,
            needleValue: this.coLevel
          }]
        },
        options: {
          rotation: -90,
          circumference: 180,
          cutout: "80%",
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } }
        },
        plugins: [needlePlugin]
      })
    },
    updateGauge() {
      this.chart.data.datasets[0].needleValue = this.coLevel
      this.chart.update()
    }
  }
}
</script>

<style scoped>
.card {
  background: #ffffff;
  padding: 18px;
  border-radius: 16px;
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h3 {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  color: #334155;
}

.status-indicator {
  padding: 4px 10px;
  border-radius: 8px;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
}

.gauge-section {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 10px 0;
}

.gauge-container {
  width: 100%;
  height: 100px;
}

.value-display {
  margin-top: -20px;
}

.value {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
}

.unit {
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
  margin-left: 2px;
}

.description {
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  margin: 0;
}

.low { background: #10b981; }
.medium { background: #f59e0b; }
.high { background: #ef4444; }
</style>