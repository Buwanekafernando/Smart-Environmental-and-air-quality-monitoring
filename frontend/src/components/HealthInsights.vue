<template>
<div class="health-card" :style="{ borderLeft: healthRisk ? '6px solid ' + healthRisk.color : 'none' }">
  <div class="card-header">
    <h2>🏥 Room Health & Insights</h2>
    <div v-if="healthRisk" class="risk-label" :style="{ color: healthRisk.color }">
      {{ healthRisk.status }}
    </div>
  </div>
  
  <div class="health-grid">
    <div class="status-box">
      <div class="status-content" :style="{ color: healthRisk ? healthRisk.color : '#888' }">
        <span class="status-text">{{ healthRisk ? healthRisk.status : "..." }}</span>
      </div>
      <p class="sub-label">Current Risk</p>
    </div>
    
    <div class="health-details">
      <p class="summary" v-if="healthRisk">
        {{ getSummaryText }}
      </p>
      
      <div class="progress-section">
        <div class="health-bar">
          <div class="health-fill" :style="{ background: healthRisk ? healthRisk.color : '#cbd5e1', width: healthProgress }"></div>
        </div>
      </div>
      
      <div class="action-plan">
        <p class="plan-title">Action Plan:</p>
        <ul class="suggestions">
          <li v-for="suggestion in dynamicSuggestions" :key="suggestion">{{ suggestion }}</li>
        </ul>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    healthRisk: { type: Object, default: null },
    trendsData: { type: Object, default: null }
  },
  computed: {
    healthProgress() {
      if (!this.healthRisk) return '100%';
      if (this.healthRisk.status === 'SAFE') return '100%';
      if (this.healthRisk.status === 'MODERATE') return '60%';
      return '25%';
    },
    getSummaryText() {
      if (!this.healthRisk) return 'Waiting for data...';
      if (this.healthRisk.status === 'SAFE') return 'Environment is optimal for health.';
      if (this.healthRisk.status === 'MODERATE') return 'Slight pollution detected. Improving ventilation is recommended.';
      return 'CRITICAL! High toxin levels detected. Evacuate or ventilate immediately!';
    },
    dynamicSuggestions() {
      if (!this.healthRisk) return ['Loading...'];
      
      if (this.healthRisk.status === 'SAFE') {
        return ['Maintain cleanliness', 'Normal ventilation', 'System monitoring', 'Safe environment'];
      } else if (this.healthRisk.status === 'MODERATE') {
        return ['Open windows', 'Air purifier ON', 'Check air flow', 'Limit activity'];
      } else {
        return ['IMMEDIATE VENTILATION', 'EVACUATE IF NECESSARY', 'Check CO sources', 'High-speed filtration'];
      }
    }
  }
}
</script>

<style scoped>
.health-card {
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

.risk-label {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
}

.health-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
  flex: 1;
}

.status-box {
  background: #f8fafc;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.status-text {
  font-size: 1.4rem;
  font-weight: 800;
}

.sub-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: #94a3b8;
  margin: 5px 0 0 0;
  text-transform: uppercase;
}

.health-details {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.summary {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin: 0 0 10px 0;
}

.health-bar {
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 15px;
}

.health-fill {
  height: 100%;
  transition: width 1s ease;
}

.action-plan {
  background: #f1f5f9;
  padding: 10px;
  border-radius: 10px;
}

.plan-title {
  font-size: 0.65rem;
  font-weight: 800;
  color: #64748b;
  margin: 0 0 5px 0;
  text-transform: uppercase;
}

.suggestions {
  margin: 0;
  padding: 0;
  font-size: 0.75rem;
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
}

.suggestions li {
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 5px;
}

.suggestions li::before {
  content: "✓";
  color: #10b981;
  font-weight: 900;
}
</style>