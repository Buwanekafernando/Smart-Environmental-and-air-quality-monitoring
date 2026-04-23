<template>
<div class="dashboard-wrapper">
  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="logo">🧪</div>
    <div class="nav-icons">
      <div class="nav-item" :class="{active: activeTab==='overview'}" @click="scrollTo('overview')" title="Overview">📊</div>
      <div class="nav-item" :class="{active: activeTab==='air-quality'}" @click="scrollTo('air-quality')" title="Air Quality">🌬</div>
      <div class="nav-item" :class="{active: activeTab==='co-monitoring'}" @click="scrollTo('co-monitoring')" title="CO & Temp">🌡</div>
      <div class="nav-item" :class="{active: activeTab==='health'}" @click="scrollTo('health')" title="Room Health">🏥</div>
      <div class="nav-item" :class="{active: activeTab==='pollution'}" @click="scrollTo('pollution')" title="Reports">📄</div>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="header">
      <h1>Intelligent Environment Monitoring</h1>
      <div class="alerts-container">
        <SmokeAlert :coAnalysis="coAnalysis" :isFire="isFireAlert"/>
      </div>
    </header>

    <!-- Fire Overlay Popup -->
    <transition name="fade">
      <div v-if="isFireAlert" class="fire-overlay">
        <div class="fire-content">
          <div class="fire-icon">🔥</div>
          <h2>EXTREME DANGER DETECTED</h2>
          <p>Critical CO Spikes + High Temperature + Poor AQI</p>
          <div class="fire-metrics">
            <span>TEMP: {{ latestTemperature }}°C</span>
            <span>CO: {{ latestCO }}%</span>
            <span>AQI: {{ aqiData.score }}</span>
          </div>
          <button @click="dismissFireAlert" class="dismiss-btn">MUTE ALARM</button>
        </div>
      </div>
    </transition>

    <div class="dashboard-grid">
      <!-- Top Left: Large Chart -->
      <div class="grid-item aqi-section">
        <AirQualityChart :aqiTrend="aqiTrend" :currentAqi="aqiData" :labels="timeLabels" :trendsData="trendsData"/>
      </div>

      <!-- Top Right: Temp -->
      <div class="grid-item temp-section">
        <TemperatureCard :temperature="latestTemperature"/>
      </div>

      <!-- Middle Left: Health -->
      <div class="grid-item health-section">
        <HealthInsights :healthRisk="healthRisk" :trendsData="trendsData"/>
      </div>

      <!-- Middle Right: CO -->
      <div class="grid-item co-section">
        <COGauge :coLevel="latestCO" :coAnalysis="coAnalysis"/>
      </div>

      <!-- Bottom Row -->
      <div class="grid-item humidity-section">
        <HumidityChart :humidityTrend="humidityTrend" :labels="timeLabels"/>
      </div>

      <div class="grid-item smoke-status-section">
        <SmokingStatus :motion="latestMotion"/>
      </div>

      <div class="grid-item cost-section">
        <CostPollution :cost="estimatedCost"/>
      </div>
    </div>
    
    <ChatBot/>
  </main>
</div>
</template>

<script>
import SmokeAlert from "..\\components\\SmokeAlert.vue"
import AirQualityChart from "..\\components\\AirQualityChart.vue"
import HumidityChart from "../components/HumidityChart.vue"
import TemperatureCard from "../components/TemperatureCard.vue"
import COGauge from "../components/COGauge.vue"
import HealthInsights from "../components/HealthInsights.vue"
import SmokingStatus from "../components/SmokingStatus.vue"
import CostPollution from "../components/CostPollution.vue"
import ChatBot from "../components/ChatBot.vue"
import axios from "axios";

export default {
  name: "Dashboard",
  components: {
    SmokeAlert,
    AirQualityChart,
    HumidityChart,
    TemperatureCard,
    COGauge,
    HealthInsights,
    SmokingStatus,
    CostPollution,
    ChatBot
  },
  data() {
    return {
      sensorData: [],
      trendsData: null,
      healthRisk: null,
      coAnalysis: null,
      activeTab: 'overview',
      audioCtx: null,
      oscillator: null,
      isMuted: false
    };
  },
  computed: {
    latestRecord() {
      return this.sensorData.length > 0 ? this.sensorData[0] : null;
    },
    latestTemperature() {
      return this.latestRecord ? this.latestRecord.temperature : 0;
    },
    latestCO() {
      if (!this.latestRecord) return 0;
      let rawCO = this.latestRecord.co_level;
      return Math.min(Math.round(rawCO), 100);
    },
    latestMotion() {
      return this.latestRecord ? this.latestRecord.motion_detected : 0;
    },
    aqiData() {
      if (!this.latestRecord) return { score: 0, label: "Loading...", color: "#888" };
      let score = Math.floor(this.latestRecord.air_quality);
      
      let label = "Good";
      let color = "#22c55e"; 
      
      if (score > 300) { label = "Hazardous"; color = "#7f1d1d"; }
      else if (score > 200) { label = "Very Unhealthy"; color = "#991b1b"; }
      else if (score > 150) { label = "Unhealthy"; color = "#ef4444"; }
      else if (score > 100) { label = "Unhealthy for Sensitive Grps"; color = "#f97316"; }
      else if (score > 50) { label = "Moderate"; color = "#eab308"; }
      return { score, label, color };
    },
    aqiTrend() {
      return [...this.sensorData].reverse().map(d => Math.floor(d.air_quality));
    },
    humidityTrend() {
      return [...this.sensorData].reverse().map(d => d.humidity);
    },
    timeLabels() {
      return [...this.sensorData].reverse().map(d => {
        let date = new Date(d.timestamp * 1000); 
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      });
    },
    estimatedCost() {
      if (this.sensorData.length === 0) return 0;
      // Calculate cumulative environmental impact cost based on CO levels
      let totalCO = this.sensorData.reduce((acc, curr) => acc + curr.co_level, 0);
      return totalCO * 1.25; // Rs. 1.25 per unit of CO emission recorded
    },
    isFireAlert() {
      // Intelligent Fire Detection: CO > 70%, Temp > 40C, AQI > 250
      return this.latestCO > 70 && this.latestTemperature > 40 && this.aqiData.score > 250 && !this.isMuted;
    }
  },
  watch: {
    isFireAlert(val) {
      if (val) {
        this.playAlarm();
      } else {
        this.stopAlarm();
      }
    }
  },
  mounted() {
    this.fetchData();
    setInterval(this.fetchData, 3000);
  },
  methods: {
    scrollTo(id) {
      this.activeTab = id;
      // Scroller logic removed since we don't want scrolling
    },
    async fetchData() {
      try {
        const [resData, resTrends, resHealth, resCo] = await Promise.all([
          axios.get("http://localhost:5000/api/data"),
          axios.get("http://localhost:5000/api/trends"),
          axios.get("http://localhost:5000/api/health-risk"),
          axios.get("http://localhost:5000/api/co-analysis")
        ]);
        this.sensorData = resData.data;
        this.trendsData = resTrends.data;
        this.healthRisk = resHealth.data;
        this.coAnalysis = resCo.data;
      } catch (error) {
        console.error("Error fetching sensor data:", error);
      }
    },
    playAlarm() {
      if (this.audioCtx) return;
      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      this.oscillator = this.audioCtx.createOscillator();
      const gainNode = this.audioCtx.createGain();
      
      this.oscillator.type = 'sawtooth';
      this.oscillator.frequency.setValueAtTime(440, this.audioCtx.currentTime);
      this.oscillator.frequency.exponentialRampToValueAtTime(880, this.audioCtx.currentTime + 0.5);
      
      gainNode.gain.setValueAtTime(0.1, this.audioCtx.currentTime);
      
      this.oscillator.connect(gainNode);
      gainNode.connect(this.audioCtx.destination);
      
      this.oscillator.loop = true;
      this.oscillator.start();
      
      // Siren effect
      this.sirenInterval = setInterval(() => {
        if (this.oscillator) {
          let freq = this.oscillator.frequency.value === 440 ? 880 : 440;
          this.oscillator.frequency.exponentialRampToValueAtTime(freq, this.audioCtx.currentTime + 0.2);
        }
      }, 500);
    },
    stopAlarm() {
      if (this.oscillator) {
        this.oscillator.stop();
        this.oscillator = null;
      }
      if (this.audioCtx) {
        this.audioCtx.close();
        this.audioCtx = null;
      }
      clearInterval(this.sirenInterval);
    },
    dismissFireAlert() {
      this.isMuted = true;
      this.stopAlarm();
      // Auto-unmute after 30 seconds if conditions persist
      setTimeout(() => { this.isMuted = false; }, 30000);
  }
}
</script>

<style scoped>
.fire-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(127, 29, 29, 0.9);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.fire-content {
  background: white;
  padding: 40px;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  max-width: 500px;
  animation: shake 0.5s infinite;
}

@keyframes shake {
  0% { transform: translate(1px, 1px) rotate(0deg); }
  10% { transform: translate(-1px, -2px) rotate(-1deg); }
  20% { transform: translate(-3px, 0px) rotate(1deg); }
  30% { transform: translate(3px, 2px) rotate(0deg); }
  40% { transform: translate(1px, -1px) rotate(1deg); }
  50% { transform: translate(-1px, 2px) rotate(-1deg); }
  60% { transform: translate(-3px, 1px) rotate(0deg); }
  70% { transform: translate(3px, 1px) rotate(-1deg); }
  80% { transform: translate(-1px, -1px) rotate(1deg); }
  90% { transform: translate(1px, 2px) rotate(0deg); }
  100% { transform: translate(1px, -2px) rotate(-1deg); }
}

.fire-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.fire-content h2 {
  color: #b91c1c;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 10px;
}

.fire-metrics {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 20px 0;
  font-weight: 700;
  color: #4b5563;
}

.dismiss-btn {
  background: #1e293b;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.dismiss-btn:hover {
  background: #0f172a;
  transform: scale(1.05);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.dashboard-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #f8fafc;
}

.sidebar {
  width: 70px; /* Slightly wider sidebar */
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px 0;
  border-right: 1px solid #e2e8f0;
  box-shadow: 4px 0 10px rgba(0,0,0,0.02);
}

.logo {
  font-size: 28px;
  margin-bottom: 40px;
}

.nav-icons {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.nav-item {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  cursor: pointer;
  font-size: 22px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
}

.nav-item.active {
  background: #2b5cff;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(43, 92, 255, 0.3);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px 20px;
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.dashboard-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 2.8fr 2.2fr 1.5fr; /* Adjusted for better chart space */
  gap: 15px;
  min-height: 0;
}

.grid-item {
  background: white;
  border-radius: 16px; /* Rounder corners for premium look */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
}

.grid-item:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
}

/* Section Specific Grid Placement */
.aqi-section {
  grid-column: span 2;
}

.temp-section {
  grid-column: 3;
}

.health-section {
  grid-column: span 2;
}

.co-section {
  grid-column: 3;
}

.humidity-section {
  /* Bottom row */
}

.smoke-status-section {
  /* Bottom row */
}

.cost-section {
  /* Bottom row */
}

@media (max-width: 1200px) {
  /* We maintain the grid but maybe simplify if needed */
}
</style>