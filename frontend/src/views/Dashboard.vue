<template>

<div class="dashboard">

<!-- Alert -->
<SmokeAlert/>

<!-- Top Section -->
<div class="grid-top">

<div class="chart-card">
<AirQualityChart/>
</div>

<div class="aqi-card">
<h2>42</h2>
<p>AQI Score</p>

<div class="aqi-bar">
<div class="aqi-fill"></div>
</div>

<span class="aqi-status">Bad</span>

</div>

</div>

<!-- Sensors -->
<div class="grid-two">

<TemperatureCard/>

<COGauge/>

</div>

<!-- Health Insights -->
<HealthInsights/>

<!-- Smoking Status -->
<SmokingStatus/>

<!-- Cost -->
<CostPollution/>

<ChatBot/>

</div>

</template>
<script>
import SmokeAlert from "..\\components\\SmokeAlert.vue"
import AirQualityChart from "..\\components\\AirQualityChart.vue"
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