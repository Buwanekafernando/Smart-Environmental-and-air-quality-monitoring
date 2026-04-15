<template>

<div class="dashboard">

<!-- Alert -->
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

<!-- Humidity -->
<div class="chart-card" style="margin-top: 25px;">
<HumidityChart :humidityTrend="humidityTrend" :labels="timeLabels"/>
</div>

<!-- Smoking Status -->
<SmokingStatus :motion="latestMotion"/>

<!-- Cost -->
<CostPollution/>

<ChatBot/>

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
      sensorData: []
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
      // Scale CO raw value (100-2000) to percentage for gauge (0-100)
      if (!this.latestRecord) return 0;
      let rawCO = this.latestRecord.co_level;
      let percent = (rawCO / 2000) * 100;
      return Math.min(Math.round(percent), 100);
    },
    latestMotion() {
      return this.latestRecord ? this.latestRecord.motion_detected : 0;
    },
    aqiData() {
      if (!this.latestRecord) return { score: 0, label: "Loading...", color: "#888" };
      let raw = this.latestRecord.air_quality;
      // Convert raw MQ-135 to AQI (threshold based mapping)
      let score = Math.floor((raw / 3000) * 500); 
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
      return [...this.sensorData].reverse().map(d => Math.floor((d.air_quality / 3000) * 500));
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
        const res = await axios.get("http://localhost:5000/api/data");
        this.sensorData = res.data;
      } catch (error) {
        console.error("Error fetching sensor data:", error);
      }
    }
  }
}
</script>

<style>

.dashboard{
  padding:30px;
  font-family:Arial;
}

.cards{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:20px;
}

.card{
background:white;
border-radius:16px;
padding:25px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);
}

.row{
display:grid;
grid-template-columns:1fr 1fr;
gap:20px;
margin-top:30px;
}

.dashboard{
max-width:1200px;
margin:auto;
padding:30px;
}

.grid-two{
display:grid;
grid-template-columns:1fr 1fr;
gap:25px;
margin-top:25px;
}

@media (max-width:900px){

.grid-two{
grid-template-columns:1fr;
}

}

.dashboard{
background:#dbe7f3;
min-height:100vh;
padding:40px;
}

.gauge-container{
width:200px;
margin:auto;
}


</style>