<template>
<div class="card">
  <h3>🌡 Room Temperature</h3>
  <div class="thermometer-container">
    <div class="thermometer">
      <div class="thermometer-stem">
        <!-- The mercury column filling the stem based on % (0-50°C scale) -->
        <div class="thermometer-fill" :style="{ height: Math.min((temperature / 50) * 100, 100) + '%' }"></div>
      </div>
      <div class="thermometer-bulb"></div>
    </div>
    
    <div class="temp-text">
      <div class="temp-value">{{ temperature }}°C</div>
      <p>Current Temp</p>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    temperature: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style scoped>
.card {
  background: white;
  padding: 25px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.thermometer-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  margin-top: 20px;
}

.thermometer {
  position: relative;
  width: 30px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

.thermometer-stem {
  width: 14px;
  height: 90px;
  background: #eee;
  border-radius: 10px 10px 0 0;
  position: relative;
  z-index: 1;
  border: 2px solid #ddd;
  border-bottom: none;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.thermometer-fill {
  width: 100%;
  background: #ef4444; /* red mercury */
  transition: height 0.5s ease-in-out;
}

.thermometer-bulb {
  width: 30px;
  height: 30px;
  background: #ef4444;
  border-radius: 50%;
  position: relative;
  z-index: 2;
  margin-top: -10px;
  border: 2px solid #ddd;
}

.temp-text {
  text-align: left;
}

.temp-value {
  font-size: 40px;
  color: #ef4444;
  font-weight: bold;
}
</style>