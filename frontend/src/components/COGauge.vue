<template>

<div class="card">

<h3>⚡ CO Gas Amount in the Room</h3>

<div class="gauge-container">

<canvas ref="gaugeCanvas"></canvas>

</div>

<div class="value">{{coLevel}}%</div>

<div class="status" :class="statusClass">
{{statusText}}
</div>

</div>

</template>

<script>

import {
Chart,
ArcElement,
Tooltip
} from "chart.js"

Chart.register(ArcElement, Tooltip)

export default{

data(){
return{
coLevel:65,
chart:null
}
},

computed:{

statusText(){

if(this.coLevel<40) return "Low"
if(this.coLevel<70) return "Medium"
return "High"

},

statusClass(){

if(this.coLevel<40) return "low"
if(this.coLevel<70) return "medium"
return "high"

}

},

mounted(){

this.createGauge()

setInterval(()=>{

this.coLevel = 30 + Math.floor(Math.random()*60)

this.updateGauge()

},5000)

},

methods:{

createGauge(){

const ctx=this.$refs.gaugeCanvas.getContext("2d")

const needlePlugin={

id:"needle",

afterDatasetDraw(chart){

const {ctx}=chart
const needleValue=chart.config.data.datasets[0].needleValue
const angle=Math.PI + (needleValue/100)*Math.PI

const cx=chart.getDatasetMeta(0).data[0].x
const cy=chart.getDatasetMeta(0).data[0].y

ctx.save()

ctx.translate(cx,cy)
ctx.rotate(angle)

ctx.beginPath()
ctx.moveTo(0,-2)
ctx.lineTo(80,0)
ctx.lineTo(0,2)
ctx.fillStyle="#7c3aed"
ctx.fill()

ctx.restore()

ctx.beginPath()
ctx.arc(cx,cy,5,0,2*Math.PI)
ctx.fill()

}

}

this.chart=new Chart(ctx,{

type:"doughnut",

data:{
datasets:[
{
data:[40,30,30],
backgroundColor:["#22c55e","#f59e0b","#ef4444"],
borderWidth:0,
needleValue:this.coLevel
}
]
},

options:{
rotation:-90,
circumference:180,
cutout:"70%",
plugins:{legend:{display:false}}
},

plugins:[needlePlugin]

})

},

updateGauge(){

this.chart.data.datasets[0].needleValue=this.coLevel
this.chart.update()

}

}

}

</script>

<style>

.card{
background:#f5f5f5;
padding:25px;
border-radius:15px;
text-align:center;
}

.gauge-container{
width:220px;
margin:auto;
}

.value{
font-size:28px;
margin-top:10px;
}

.status{
margin-top:8px;
padding:5px 15px;
border-radius:20px;
display:inline-block;
color:white;
}

.low{
background:#22c55e;
}

.medium{
background:#f59e0b;
}

.high{
background:#ef4444;
}

</style>