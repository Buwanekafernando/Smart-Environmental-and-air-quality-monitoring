<template>

<div class="cost-section">

<div class="cost-card">

<h3>Cost of Pollution (Estimated Target)</h3>

<div class="cost-value">
Rs. {{ cost.toFixed(2) }}
</div>

<canvas id="pollutionChart"></canvas>

</div>

<div class="report-card">

<button @click="downloadPDF" class="print-btn">
🖨 Print Report
</button>

</div>

</div>

</template>

<script>

import jsPDF from "jspdf"
import html2canvas from "html2canvas"

export default{
props: {
  cost: {
    type: Number,
    default: 1500
  }
},

methods:{

async downloadPDF(){

const element = document.body

const canvas = await html2canvas(element)

const img = canvas.toDataURL("image/png")

const pdf = new jsPDF()

pdf.addImage(img,"PNG",10,10,190,0)

pdf.save("AirQualityReport.pdf")

}

}

}

</script>

<style>

.cost-section{
display:grid;
grid-template-columns:2fr 1fr;
gap:20px;
margin-top:30px;
}

.cost-card{
background:#f5f5f5;
padding:25px;
border-radius:15px;
text-align:center;
}

.cost-value{
font-size:30px;
color:#2b7cff;
margin:15px 0;
}

.report-card{
display:flex;
align-items:center;
justify-content:center;
}

.print-btn{
background:#2b7cff;
color:white;
border:none;
padding:12px 25px;
border-radius:10px;
cursor:pointer;
}

</style>