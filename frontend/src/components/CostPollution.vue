<template>
<div class="cost-card">
  <div class="header-info">
    <span class="label">Real-time Impact Cost</span>
  </div>
  
  <div class="metrics-grid">
    <div class="metric highlight">
      <span class="metric-label">Total Cost</span>
      <div class="amount">
        <span class="currency">Rs.</span>
        <span class="value">{{ (costData?.total_cost || 0).toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}) }}</span>
      </div>
    </div>
    
    <div class="metric">
      <span class="metric-label">Total Emission</span>
      <div class="amount">
        <span class="value">{{ (costData?.total_emission || 0).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }}</span>
        <span class="currency ml-1">%</span>
      </div>
    </div>

    <div class="metric">
      <span class="metric-label">Avg Cost</span>
      <div class="amount">
        <span class="currency">Rs.</span>
        <span class="value">{{ (costData?.avg_cost || 0).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }}</span>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    costData: { 
      type: Object, 
      default: () => ({ total_cost: 0, total_emission: 0, avg_cost: 0 }) 
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
  margin-bottom: 15px;
  display: block;
}

.metrics-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
}

.metric.highlight {
  background: white;
  border: 1px solid #93c5fd;
  padding: 12px;
}

.metric-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #3b82f6;
}

.metric.highlight .metric-label {
  color: #1e40af;
  font-weight: 700;
}

.amount {
  color: #1e40af;
  display: flex;
  align-items: baseline;
}

.currency {
  font-size: 0.85rem;
  font-weight: 700;
  margin-right: 4px;
}

.ml-1 {
  margin-left: 4px;
  margin-right: 0;
}

.metric.highlight .currency {
  font-size: 1rem;
}

.value {
  font-size: 1.2rem;
  font-weight: 800;
  line-height: 1;
}

.metric.highlight .value {
  font-size: 1.8rem;
}
</style>