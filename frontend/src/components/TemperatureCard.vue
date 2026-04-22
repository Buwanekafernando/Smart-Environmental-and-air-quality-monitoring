<template>
<div class="card">
  <div class="card-header">
    <h3>🌡 Temperature</h3>
  </div>
  
  <div class="content-section">
    <div class="thermometer-container">
      <div class="thermometer">
        <div class="thermometer-stem">
          <div class="thermometer-fill" :style="{ height: Math.min((temperature / 50) * 100, 100) + '%' }"></div>
        </div>
        <div class="thermometer-bulb"></div>
      </div>
    </div>
    
    <div class="temp-display">
      <div class="temp-value">{{ temperature }}<span class="unit">°C</span></div>
      <p class="label">Current Reading</p>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    temperature: { type: Number, default: 0 }
  }
}
</script>

<style scoped>
.card {
  background: white;
  padding: 18px;
  border-radius: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header h3 {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  color: #334155;
}

.content-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 25px;
  margin-top: 10px;
}

.thermometer {
  position: relative;
  width: 24px;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

.thermometer-stem {
  width: 12px;
  height: 80px;
  background: #f1f5f9;
  border-radius: 6px 6px 0 0;
  position: relative;
  z-index: 1;
  border: 1.5px solid #e2e8f0;
  border-bottom: none;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.thermometer-fill {
  width: 100%;
  background: linear-gradient(to top, #ef4444, #f87171);
  transition: height 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.thermometer-bulb {
  width: 24px;
  height: 24px;
  background: #ef4444;
  border-radius: 50%;
  position: relative;
  z-index: 2;
  margin-top: -8px;
  border: 1.5px solid #e2e8f0;
}

.temp-display {
  text-align: left;
}

.temp-value {
  font-size: 2.2rem;
  color: #ef4444;
  font-weight: 800;
  line-height: 1;
}

.temp-value .unit {
  font-size: 1rem;
  margin-left: 2px;
}

.label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  margin: 5px 0 0 0;
}
</style>