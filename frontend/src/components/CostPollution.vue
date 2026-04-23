<template>
<div class="cost-card">
  <div class="header-info">
    <span class="label">Real-time Impact Cost</span>
  </div>
  <div class="cost-body">
    <div class="amount">
      <span class="currency">Rs.</span>
      <span class="value">{{ cost.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}) }}</span>
    </div>
    <button @click="downloadPDF" class="print-btn">
      <span>📄 Report</span>
    </button>
  </div>
</div>
</template>

<script>
import jsPDF from "jspdf"
import html2canvas from "html2canvas"

export default {
  props: {
    cost: { type: Number, default: 1500 }
  },
  methods: {
    async downloadPDF() {
      const element = document.body
      const canvas = await html2canvas(element)
      const img = canvas.toDataURL("image/png")
      const pdf = new jsPDF()
      pdf.addImage(img, "PNG", 10, 10, 190, 0)
      pdf.save("AirQualityReport.pdf")
    }
  }
}
</script>

<style scoped>
.cost-card {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  padding: 18px;
  border-radius: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid #bfdbfe;
}

.label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #1e40af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.cost-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.amount {
  color: #1e40af;
  display: flex;
  align-items: baseline;
}

.currency {
  font-size: 1rem;
  font-weight: 700;
  margin-right: 4px;
}

.value {
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1;
}

.print-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 700;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
}

.print-btn:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
}
</style>