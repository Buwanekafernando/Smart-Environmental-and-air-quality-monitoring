<template>

<div class="air-card">

  <div class="chart-section">

    <h2>🌬 Air Quality</h2>

    <Line :data="chartData" :options="chartOptions"/>

  </div>

  <div class="score-section">

    <h1 :style="{ color: currentAqi ? currentAqi.color : '#000' }">{{ currentAqi ? currentAqi.score : 0 }}</h1>
    <p>AQI Score</p>

    <div class="aqi-bar" style="background: #ddd; height: 10px; border-radius: 5px; margin-top: 20px; overflow: hidden;">
      <div class="aqi-fill" :style="{ backgroundColor: currentAqi ? currentAqi.color : '#ddd', width: Math.min(((currentAqi ? currentAqi.score : 0) / 5), 100) + '%', height: '100%', borderRadius: '5px', transition: 'width 0.5s ease-in-out' }"></div>
    </div>

    <button class="status" :style="{ backgroundColor: currentAqi ? currentAqi.color : '#888' }">{{ currentAqi && currentAqi.label ? currentAqi.label : 'Loading...' }}</button>

    <div v-if="trendsData" style="margin-top: 20px; text-align: left; background: white; padding: 10px; border-radius: 8px;">
      <p style="margin: 5px 0;"><strong>Trend:</strong> {{ trendsData.trend }}</p>
      <p style="margin: 5px 0;"><strong>Forecast:</strong> {{ trendsData.forecast }}</p>
    </div>

  </div>

</div>

</template>

<script>
import { Line } from "vue-chartjs"
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler
} from "chart.js"

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler
)

export default {

components:{Line},

props: {
  aqiTrend: { type: Array, default: () => [] },
  currentAqi: { type: Object, default: () => ({}) },
  labels: { type: Array, default: () => [] },
  trendsData: { type: Object, default: null }
},

data(){
return{

chartData:{
labels: [],
datasets:[
{
label:"AQI",
data: [],
borderColor:"#3b82f6",
pointRadius:3,
tension:0.4,
fill:true,
backgroundColor:(context)=>{
const chart = context.chart
const {ctx, chartArea} = chart

if(!chartArea) return null

const gradient = ctx.createLinearGradient(0,chartArea.top,0,chartArea.bottom)

gradient.addColorStop(0,"rgba(255,0,0,0.5)")
gradient.addColorStop(0.4,"rgba(255,165,0,0.5)")
gradient.addColorStop(0.7,"rgba(255,255,0,0.5)")
gradient.addColorStop(1,"rgba(0,200,0,0.5)")

return gradient
}
}
]
},

chartOptions:{
responsive:true,
plugins:{
legend:{display:false}
},
scales:{
y:{
min:0,
max:500
}
}
}

}
},
watch: {
  aqiTrend: {
    handler(newVal) {
      this.chartData = {
        ...this.chartData,
        labels: this.labels,
        datasets: [{
          ...this.chartData.datasets[0],
          data: newVal
        }]
      };
    },
    deep: true,
    immediate: true
  }
}
};
</script>

<style>

.air-card{
display:flex;
gap:40px;
background:#f3f3f3;
padding:30px;
border-radius:15px;
margin-top:30px;
}

.chart-section{
flex:2;
}

.score-section{
flex:1;
text-align:center;
}

.score-section h1{
font-size:60px;
margin:0;
}

.bar{
display:flex;
height:20px;
border-radius:20px;
overflow:hidden;
margin-top:20px;
}

.bad{
flex:1;
background:linear-gradient(to right,red,orange);
}

.good{
flex:1;
background:linear-gradient(to right,yellow,green);
}

.status{
margin-top:15px;
background:red;
color:white;
border:none;
padding:8px 20px;
border-radius:20px;
}

</style>