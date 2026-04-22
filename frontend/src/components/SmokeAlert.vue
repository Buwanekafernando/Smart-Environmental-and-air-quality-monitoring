<template>
<div class="alert-box" v-if="coAnalysis && coAnalysis.smoking_detected">
  <span class="icon">🚨</span>
  <span class="msg">Smoke/High CO Detected!</span>
</div>
</template>

<script>
export default {
  props: {
    coAnalysis: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.alert-box {
  background: #ff4b6e;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: bold;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
</style>