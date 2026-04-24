<template>
<div class="dashboard-wrapper">
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
          <h2>{{ fireAlert ? fireAlert.level : 'EXTREME DANGER DETECTED' }}</h2>
          <p>{{ fireAlert ? fireAlert.message : 'Critical CO Spikes + High Temperature + Poor AQI' }}</p>
          <div class="fire-metrics">
            <span>TEMP: {{ latestTemperature }}°C</span>
            <span>CO: {{ latestCO }}%</span>
            <span>AQI: {{ aqiData.score }}</span>
          </div>
          <button @click="dismissFireAlert" class="dismiss-btn">MUTE ALARM</button>
        </div>
      </div>
    </transition>

    <div class="dashboard-grid" id="overview">
      <!-- Row 1: Key Metrics -->
      <div class="grid-item aqi-section glass" id="air-quality">
        <AirQualityChart :aqiTrend="aqiTrend" :currentAqi="aqiData" :labels="timeLabels" :trendsData="trendsData"/>
      </div>

      <div class="grid-item temp-section glass">
        <TemperatureCard :temperature="latestTemperature"/>
      </div>

      <!-- Row 2: Secondary Metrics -->
      <div class="grid-item co-section glass" id="co-monitoring">
        <COGauge :coLevel="latestCO" :coAnalysis="coAnalysis"/>
      </div>

      <div class="grid-item humidity-section glass">
        <HumidityChart :humidityTrend="humidityTrend" :labels="timeLabels"/>
      </div>

      <div class="grid-item smoke-status-section glass">
        <SmokingStatus :motion="latestMotion"/>
      </div>

      <!-- Row 3: Insights & Costs -->
      <div class="grid-item health-section glass" id="health">
      <HealthInsights :healthRisk="liveHealthRisk" :aiStatus="aiStatus" :trendsData="trendsData"/>
      </div>

      <div class="grid-item cost-section glass">
        <CostPollution :costData="pollutionCost"/>
      </div>

      


      
      
    </div>
    
   
  
    
  </main>
</div>
</template>

<script>
import SmokeAlert from "../components/SmokeAlert.vue"
import AirQualityChart from "../components/AirQualityChart.vue"
import HumidityChart from "../components/HumidityChart.vue"
import TemperatureCard from "../components/TemperatureCard.vue"
import COGauge from "../components/COGauge.vue"
import HealthInsights from "../components/HealthInsights.vue"
import SmokingStatus from "../components/SmokingStatus.vue"
import CostPollution from "../components/CostPollution.vue"
import axios from "axios";
import { io } from "socket.io-client";

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
    Line: () => import('vue-chartjs').then(m => m.Line)
  },
  data() {
    return {
      socket: null,
      aiStatus: null,
      sensorData: [],
      trendsData: null,
      healthRisk: null,
      coAnalysis: null,
      pollutionCost: null,
      fireAlert: null,
      audioCtx: null,
      oscillator: null,
      gainNode: null,
      sirenInterval: null,
      _sirenHigh: false,       // tracks current frequency toggle state
      isMuted: false,
      miniChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { display: false },
          x: { display: false }
        }
      }
    };
  },
  computed: {
    latestRecord() {
      return this.sensorData.length > 0 ? this.sensorData[0] : null;
    },
    latestTemperature() {
      return this.latestRecord ? parseFloat(this.latestRecord.temperature) || 0 : 0;
    },
    latestCO() {
      if (!this.latestRecord) return 0;
      return parseFloat(this.latestRecord.co_percent) || 0;
    },
    latestHumidity() {
      // ✅ Always pull from the newest record (sensorData[0])
      return this.latestRecord ? parseFloat(this.latestRecord.humidity) || 0 : 0;
    },
    latestMotion() {
      return this.latestRecord ? (this.latestRecord.motion === true || this.latestRecord.motion === "true" ? 1 : 0) : 0;
    },
    // ✅ Computed live health risk — updates on every WebSocket message
    liveHealthRisk() {
      if (!this.latestRecord) return { status: 'Loading...', color: '#888' };
      const aqi = parseFloat(this.latestRecord.aqi_numeric) || 0;
      const co  = parseFloat(this.latestRecord.co_percent)  || 0;
      if (aqi > 200 || co > 70) return { status: 'UNSAFE',   color: 'red' };
      if (aqi > 80  || co > 40) return { status: 'MODERATE', color: '#f59e0b' };
      return { status: 'SAFE', color: 'green' };
    },
    aqiData() {
      if (!this.latestRecord) return { score: 0, label: "Loading...", color: "#888" };
      
      // ✅ Use numeric aqi_numeric from backend
      let score = parseInt(this.latestRecord.aqi_numeric) || 0;
      
      let label = "Good";
      let color = "#22c55e"; 
      
      if (score > 200) { label = "Hazardous"; color = "#7f1d1d"; }
      else if (score > 100) { label = "Bad"; color = "#ef4444"; }
      else if (score > 50) { label = "Fair"; color = "#eab308"; }
      
      return { score, label, color };
    },
    aqiTrend() {
      return [...this.sensorData].reverse().map(d => parseInt(d.aqi_numeric) || 0);
    },
    humidityTrend() {
      return [...this.sensorData].reverse().map(d => parseFloat(d.humidity) || 0);
    },
    timeLabels() {
      return [...this.sensorData].reverse().map(d => {
        let date = new Date(d.timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      });
    },
    estimatedCost() {
      return this.pollutionCost ? this.pollutionCost.total_cost : 0;
    },
    coTrend() {
      return [...this.sensorData].reverse().map(d => parseFloat(d.co_percent) || 0);
    },
    costTrend() {
      // For simplicity, we'll map co_percent to a cost factor for the trend chart
      return [...this.sensorData].reverse().map(d => (parseFloat(d.co_percent) || 0) * 0.5);
    },
    aqiChartData() {
      return {
        labels: this.timeLabels,
        datasets: [{
          data: this.aqiTrend,
          borderColor: "#2563eb",
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2,
          fill: true,
          backgroundColor: "rgba(37, 99, 235, 0.1)"
        }]
      };
    },
    coChartData() {
      return {
        labels: this.timeLabels,
        datasets: [{
          data: this.coTrend,
          borderColor: "#d97706",
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2,
          fill: true,
          backgroundColor: "rgba(217, 119, 6, 0.1)"
        }]
      };
    },
    costChartData() {
      return {
        labels: this.timeLabels,
        datasets: [{
          data: this.costTrend,
          borderColor: "#059669",
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2,
          fill: true,
          backgroundColor: "rgba(5, 150, 105, 0.1)"
        }]
      };
    },
    isFireAlert() {
      return this.fireAlert ? (this.fireAlert.alert && !this.isMuted) : false;
    },
  },
  watch: {
    isFireAlert: {
      // immediate:true ensures the alarm fires on first load
      // if alert is already active when the page mounts
      immediate: true,
      handler(val) {
        if (val) {
          this.playAlarm();
        } else {
          this.stopAlarm();
        }
      }
    }
  },
  mounted() {
    this.setupSocket();
    this.initialLoad();
  },
  methods: {
    setupSocket() {
      this.socket = io("http://localhost:5000");

      this.socket.on("connect", () => {
        console.log("✅ WebSocket connected");
      });

      this.socket.on("disconnect", () => {
        console.warn("⚠️ WebSocket disconnected");
      });

      this.socket.on("sensor_update", (data) => {
        if (!data) return;

        // ✅ Fixed dedup: compare by timestamp instead of _id (which may not exist on raw data)
        const latestTimestamp = this.sensorData.length > 0 ? this.sensorData[0].timestamp : null;
        const isNewReading = !latestTimestamp || data.timestamp !== latestTimestamp;

        if (isNewReading) {
          this.sensorData.unshift(data);
          if (this.sensorData.length > 1800) {
            this.sensorData.pop();
          }
        }

        if (data.ai_status) {
          this.aiStatus = data.ai_status;
        }

        // ✅ Instant fire alert via WebSocket — no need to wait for 5s poll
        if (data.fire_alert !== undefined) {
          this.fireAlert = data.fire_alert;
        }
      });
    },
    async initialLoad() {
      try {
        // Initial fetch of historical data
        const resData = await axios.get("http://localhost:5000/api/data");
        this.sensorData = resData.data;
        
        if (this.sensorData.length && this.sensorData[0].ai_status) {
          this.aiStatus = this.sensorData[0].ai_status;
        }

        // Fetch analytical data once
        await this.fetchUpdates();

        // Poll aggregated analytics every 5s
        setInterval(this.fetchUpdates, 5000);

        // ✅ Fallback: poll latest sensor every 2s to keep live values updating
        setInterval(this.fetchLatestSensor, 2000);
      } catch (error) {
        console.error("Error during initial load:", error);
      }
    },
    async fetchLatestSensor() {
      try {
        const res = await axios.get("http://localhost:5000/api/data/latest");
        const data = res.data;
        if (!data || !data.timestamp) return;

        const latestTimestamp = this.sensorData.length > 0 ? this.sensorData[0].timestamp : null;
        if (data.timestamp !== latestTimestamp) {
          this.sensorData.unshift(data);
          if (this.sensorData.length > 1800) {
            this.sensorData.pop();
          }
          if (data.ai_status) {
            this.aiStatus = data.ai_status;
          }
        }
      } catch (error) {
        // Silently ignore polling errors to avoid console spam
      }
    },
    async fetchUpdates() {
      try {
        const [resTrends, resHealth, resCo, resCost, resFire] = await Promise.all([
          axios.get("http://localhost:5000/api/trends"),
          axios.get("http://localhost:5000/api/health-risk"),
          axios.get("http://localhost:5000/api/co-analysis"),
          axios.get("http://localhost:5000/api/pollution-cost"),
          axios.get("http://localhost:5000/api/fire-alert")
        ]);

        this.trendsData = resTrends.data;
        this.healthRisk = resHealth.data;
        this.coAnalysis = resCo.data;
        this.pollutionCost = resCost.data;
        this.fireAlert = resFire.data;
      } catch (error) {
        console.error("Error fetching updates:", error);
      }
    },
    playAlarm() {
      // ✅ Don't create a second context if one is already running
      if (this.audioCtx) {
        // Resume if browser auto-suspended it (autoplay policy)
        if (this.audioCtx.state === 'suspended') {
          this.audioCtx.resume();
        }
        return;
      }

      try {
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        this.oscillator = this.audioCtx.createOscillator();
        this.gainNode = this.audioCtx.createGain();

        this.oscillator.type = 'sawtooth';
        this.oscillator.frequency.setValueAtTime(440, this.audioCtx.currentTime);

        // Medium volume — audible but not ear-piercing
        this.gainNode.gain.setValueAtTime(0.15, this.audioCtx.currentTime);

        this.oscillator.connect(this.gainNode);
        this.gainNode.connect(this.audioCtx.destination);
        this.oscillator.start();

        // ✅ Use a flag to track freq state — reading .value is unreliable
        this._sirenHigh = false;
        this.sirenInterval = setInterval(() => {
          if (this.oscillator && this.audioCtx) {
            this._sirenHigh = !this._sirenHigh;
            const targetFreq = this._sirenHigh ? 880 : 440;
            this.oscillator.frequency.exponentialRampToValueAtTime(
              targetFreq,
              this.audioCtx.currentTime + 0.18
            );
          }
        }, 450);

        // ✅ Resume in case browser suspended it immediately after creation
        this.audioCtx.resume();
      } catch (e) {
        console.warn('Audio alarm failed to start:', e);
      }
    },
    stopAlarm() {
      clearInterval(this.sirenInterval);
      this.sirenInterval = null;
      if (this.oscillator) {
        try { this.oscillator.stop(); } catch (_) {}
        this.oscillator = null;
      }
      if (this.audioCtx) {
        try { this.audioCtx.close(); } catch (_) {}
        this.audioCtx = null;
      }
      this.gainNode = null;
      this._sirenHigh = false;
    },
    dismissFireAlert() {
      this.isMuted = true;
      this.stopAlarm();
      // Auto-unmute after 30 seconds if conditions persist
      setTimeout(() => { this.isMuted = false; }, 30000);
    }
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

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px 20px;
  overflow-y: auto;
  overflow-x: hidden;
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
  grid-template-rows: auto auto auto;
  gap: 20px;
  margin-bottom: 20px;
}

.grid-item {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.grid-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.glass {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(12px);
}



/* Section Specific Grid Placement */
.aqi-section {
  grid-column: span 2;
  min-height: 320px;
}

.temp-section {
  grid-column: 3;
}

.health-section {
  grid-column: span 2;
}

.co-section {
  grid-column: 1;
}

.humidity-section {
  grid-column: 2;
}

.smoke-status-section {
  grid-column: 3;
}

.cost-section {
  grid-column: 3;
}

.trend-card {
  padding: 15px;
  height: 120px;
}

.trend-card h3 {
  font-size: 0.75rem;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #64748b;
  text-transform: uppercase;
}

.mini-chart {
  flex: 1;
  min-height: 0;
}

@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
  }
  .aqi-section, .health-section {
    grid-column: span 2;
  }
}
</style>