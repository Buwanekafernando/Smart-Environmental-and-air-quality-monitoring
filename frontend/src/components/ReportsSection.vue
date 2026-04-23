<template>
<div class="reports-container" id="pollution">
  <div class="reports-header">
    <h2>📄 Detailed Environmental Analysis & Reports</h2>
    <button @click="generatePDF" class="download-report-btn">
      <span>📥 Download Full PDF Report</span>
    </button>
  </div>

  <div class="charts-grid">
    <div class="report-chart-card">
      <h3>🌬 Air Quality Index Trend</h3>
      <div class="chart-box">
        <Line :data="aqiChartData" :options="chartOptions" />
      </div>
    </div>

    <div class="report-chart-card">
      <h3>🌡 CO Concentration (%)</h3>
      <div class="chart-box">
        <Line :data="coChartData" :options="chartOptions" />
      </div>
    </div>

    <div class="report-chart-card">
      <h3>💰 Estimated Pollution Cost (Rs.)</h3>
      <div class="chart-box">
        <Line :data="costChartData" :options="chartOptions" />
      </div>
    </div>
  </div>

  <div class="insights-section">
    <h3>💡 Actionable Insights & Recommendations</h3>
    <div class="insights-grid">
      <div class="insight-item">
        <div class="insight-icon">🧼</div>
        <div class="insight-text">
          <h4>Maintain Cleanliness</h4>
          <p>Regular dusting and cleaning can significantly reduce particulate matter and improve AQI levels.</p>
        </div>
      </div>
      <div class="insight-item">
        <div class="insight-icon">🪟</div>
        <div class="insight-text">
          <h4>Optimize Ventilation</h4>
          <p>Open windows during low-pollution hours to ensure fresh air circulation and reduce CO buildup.</p>
        </div>
      </div>
      <div class="insight-item">
        <div class="insight-icon">🛠️</div>
        <div class="insight-text">
          <h4>Source Control</h4>
          <p>Identify and mitigate sources of CO, such as faulty heating systems or indoor smoking.</p>
        </div>
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
import jsPDF from "jspdf"
import html2canvas from "html2canvas"

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend, Filler)

export default {
  name: "ReportsSection",
  components: { Line },
  props: {
    labels: { type: Array, default: () => [] },
    aqiTrend: { type: Array, default: () => [] },
    coTrend: { type: Array, default: () => [] },
    costTrend: { type: Array, default: () => [] }
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          y: {
            grid: { color: "rgba(0,0,0,0.05)" },
            ticks: { font: { size: 10, weight: '600' } }
          },
          x: {
            grid: { display: false },
            ticks: { font: { size: 10, weight: '600' }, maxRotation: 0 }
          }
        }
      }
    }
  },
  computed: {
    aqiChartData() {
      return {
        labels: this.labels,
        datasets: [{
          label: "AQI",
          data: this.aqiTrend,
          borderColor: "#2563eb",
          backgroundColor: "rgba(37, 99, 235, 0.1)",
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 0
        }]
      }
    },
    coChartData() {
      return {
        labels: this.labels,
        datasets: [{
          label: "CO %",
          data: this.coTrend,
          borderColor: "#d97706",
          backgroundColor: "rgba(217, 119, 6, 0.1)",
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 0
        }]
      }
    },
    costChartData() {
      return {
        labels: this.labels,
        datasets: [{
          label: "Cost (Rs.)",
          data: this.costTrend,
          borderColor: "#059669",
          backgroundColor: "rgba(5, 150, 105, 0.1)",
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 0
        }]
      }
    }
  },
  methods: {
    async generatePDF() {
      const element = document.getElementById("reports-section")
      const canvas = await html2canvas(element, { scale: 2 })
      const imgData = canvas.toDataURL("image/png")
      const pdf = new jsPDF("p", "mm", "a4")
      const imgProps = pdf.getImageProperties(imgData)
      const pdfWidth = pdf.internal.pageSize.getWidth()
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width
      
      pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight)
      pdf.save("Environmental_Report.pdf")
    }
  }
}
</script>

<style scoped>
.reports-container {
  background: white;
  padding: 30px;
  border-radius: 24px;
  margin-top: 20px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.reports-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f1f5f9;
}

.reports-header h2 {
  font-size: 1.6rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.download-report-btn {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 12px rgba(30, 41, 59, 0.2);
}

.download-report-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 20px rgba(30, 41, 59, 0.3);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  margin-bottom: 40px;
}

.report-chart-card {
  background: #ffffff;
  padding: 20px;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
}

.report-chart-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  border-color: #e2e8f0;
}

.report-chart-card h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #64748b;
  margin-top: 0;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-box {
  height: 220px;
}

.insights-section {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 25px;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
}

.insights-section h3 {
  font-size: 1.2rem;
  font-weight: 800;
  color: #1e293b;
  margin-top: 0;
  margin-bottom: 25px;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.insight-item {
  display: flex;
  gap: 15px;
  align-items: flex-start;
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
  border: 1px solid #f1f5f9;
  transition: all 0.3s ease;
}

.insight-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.insight-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.insight-text h4 {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.insight-text p {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 1000px) {
  .charts-grid, .insights-grid {
    grid-template-columns: 1fr;
  }
}
</style>
