<template>
<div class="smoke-card" :class="motion === 1 ? 'smoking' : 'safe'">
  <div class="status-icon">{{ motion === 1 ? '🚨' : '🛡️' }}</div>
  <div class="status-info">
    <h3>{{ motion === 1 ? 'Presence Detected' : 'Room Secure' }}</h3>
    <p>{{ motion === 1 ? 'Motion detected in room' : 'No unusual activity' }}</p>
  </div>
</div>
</template>

<script>
export default {
  props: {
    motion: { type: Number, default: 0 }
  }
}
</script>

<style scoped>
.smoke-card {
  padding: 15px 20px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 15px;
  height: 100%;
  transition: all 0.3s ease;
}

.status-icon {
  font-size: 2.2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.status-info h3 {
  font-size: 1rem;
  font-weight: 800;
  margin: 0;
}

.status-info p {
  font-size: 0.75rem;
  font-weight: 600;
  margin: 2px 0 0 0;
  opacity: 0.9;
}

.smoking {
  background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
  border: 2px solid #fda4af;
  color: #e11d48;
  box-shadow: 0 4px 15px rgba(225, 29, 72, 0.1);
}

.safe {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 2px solid #86efac;
  color: #166534;
  box-shadow: 0 4px 15px rgba(22, 101, 52, 0.05);
}
</style>