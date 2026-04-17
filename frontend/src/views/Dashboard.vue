<template>
<div class="dashboard-wrapper">
  <!-- Sidebar -->
  <aside class="sidebar">
    <h2>🧪 LabDash</h2>
    <div class="nav-item active">Overview</div>
    <div class="nav-item">Air Quality</div>
    <div class="nav-item">CO Monitoring</div>
    <div class="nav-item">Temp & Humidity</div>
    <div class="nav-item">IR Detection</div>
    <div class="nav-item">Reports</div>
    <div class="nav-item">Alerts</div>
    <div class="nav-item">Chatbot</div>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <div class="header">
      <h1>Intelligent Environment Monitoring</h1>
    </div>

    <!-- Alert Override (Global) -->
    <SmokeAlert/>

    <!-- Top Section -->
    <div class="grid-top">
      <div class="chart-card">
        <AirQualityChart :aqiTrend="aqiTrend" :currentAqi="aqiData" :labels="timeLabels"/>
      </div>
    </div>

    <!-- Sensors -->
    <div class="grid-two">
      <TemperatureCard :temperature="latestTemperature"/>
      <COGauge :coLevel="latestCO"/>
    </div>

    <!-- Health Insights -->
    <HealthInsights/>

    <!-- Humidity & Cost -->
    <div class="grid-two">
      <div class="chart-card">
        <HumidityChart :humidityTrend="humidityTrend" :labels="timeLabels"/>
      </div>
      <CostPollution/>
    </div>

    <!-- Smoking Status -->
    <SmokingStatus :motion="latestMotion"/>
    
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
      coAnalysis: null
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
      // Scale CO raw value to percentage for gauge (0-100)
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
      let color = "#22c55e"; // green
      
      if (score > 300) {
        label = "Hazardous";
        color = "#7f1d1d"; // dark red
      } else if (score > 200) {
        label = "Very Unhealthy";
        color = "#991b1b"; // red
      } else if (score > 150) {
        label = "Unhealthy";
        color = "#ef4444"; // light red
      } else if (score > 100) {
        label = "Unhealthy for Sensitive Grps";
        color = "#f97316"; // orange
      } else if (score > 50) {
        label = "Moderate";
        color = "#eab308"; // yellow
      }
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
        let date = new Date(d.timestamp * 1000); // Assuming seconds from python time.time()
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      });
    }
  },
  mounted() {
    this.fetchData();
    setInterval(this.fetchData, 3000); // every 3 sec
  },
  methods: {
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
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background:#f4f7fb;
}

.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: white;
  padding: 30px 20px;
  box-shadow: 2px 0 10px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.sidebar h2 {
  margin-bottom: 20px;
  color: #333;
}

.nav-item {
  padding: 12px 15px;
  border-radius: 8px;
  cursor: pointer;
  color: #555;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-item:hover, .nav-item.active {
  background: #eef2f6;
  color: #2b5cff;
}

.main-content {
  flex: 1;
  padding: 30px 40px;
  overflow-y: auto;
}

.header {
  margin-bottom: 30px;
}

.header h1 {
  margin: 0;
  color: #222;
  font-size: 28px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.grid-top {
  margin-bottom: 25px;
}

.grid-two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  margin-bottom: 25px;
  margin-top: 25px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
  padding: 20px;
  margin-bottom: 25px;
}

@media (max-width: 900px) {
  .dashboard-wrapper {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
    padding: 15px;
  }
  .grid-two {
    grid-template-columns: 1fr;
  }
}

.gauge-container {
  width: 200px;
  margin: auto;
}
</style>