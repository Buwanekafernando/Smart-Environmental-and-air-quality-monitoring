<template>

<div class="air-card">

  <div class="chart-section">

    <h2>🌬 Air Quality</h2>

    <Line :data="chartData" :options="chartOptions"/>

  </div>

  <div class="score-section">

    <h1>42</h1>
    <p>AQI Score</p>

    <div class="bar">

      <div class="bad"></div>
      <div class="good"></div>

    </div>

    <button class="status">Bad</button>

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

data(){
return{

chartData:{
labels:["00:00","04:00","08:00","12:00","16:00","24:00"],
datasets:[
{
label:"AQI",
data:[85,75,45,35,40,70],
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
max:100
}
}
}

}
},
mounted(){

setInterval(()=>{

const newValue = Math.floor(Math.random()*100)

// add new value
this.chartData.datasets[0].data.push(newValue)

// remove first value
this.chartData.datasets[0].data.shift()

},3000)

}


}
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