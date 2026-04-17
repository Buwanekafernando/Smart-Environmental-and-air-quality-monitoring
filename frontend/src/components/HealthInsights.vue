<template>

<div class="health-card" :style="{ borderLeft: healthRisk ? '5px solid ' + healthRisk.color : 'none' }">

<h2>Room Health & Insights</h2>

<div class="health-grid">

<!-- Left side -->
<div class="people-card">

<h4>Current Risk Status</h4>

<div class="people-chart" :style="{ color: healthRisk ? healthRisk.color : '#888' }">
  <h3>{{ healthRisk ? healthRisk.status : "Loading..." }}</h3>
</div>

</div>

<!-- Right side -->
<div class="health-info">

<p v-if="healthRisk && healthRisk.status === 'SAFE'">
  The air quality is great, and CO levels are normal. Keep the room ventilated as usual.
</p>
<p v-else-if="healthRisk && healthRisk.status === 'MODERATE'">
  Air quality or CO levels are slightly elevated. Consider opening a window or turning on an air purifier.
</p>
<p v-else-if="healthRisk && healthRisk.status === 'UNSAFE'">
  Warning: The room environment is unsafe! High pollution or CO levels detected. Evacuate or ventilate immediately!
</p>
<p v-else>
  Gathering health data...
</p>

<div class="health-bar">
<div class="health-fill" :style="{ background: healthRisk ? healthRisk.color : '#ddd', width: healthRisk ? (healthRisk.status === 'SAFE' ? '100%' : healthRisk.status === 'MODERATE' ? '50%' : '15%') : '100%' }"></div>
</div>

<ul class="suggestions">
<li>Open window for better air circulation</li>
<li>Consider using an air purifier</li>
<li>Avoid smoking in enclosed space</li>
<li>Monitor CO levels regularly</li>
</ul>

</div>

</div>

</div>

</template>

<script>
export default {
  props: {
    healthRisk: { type: Object, default: null },
    trendsData: { type: Object, default: null }
  }
}
</script>

<style>

.health-card{
background:#f5f5f5;
padding:25px;
border-radius:15px;
margin-top:30px;
}

.health-grid{
display:grid;
grid-template-columns:1fr 2fr;
gap:20px;
}

.people-card{
background:white;
padding:20px;
border-radius:10px;
text-align:center;
}

.people-chart{
font-size:40px;
color:#ff4081;
}

.health-info p{
margin-bottom:10px;
}

.health-bar{
height:15px;
background:#ddd;
border-radius:10px;
margin:10px 0;
}

.health-fill{
height:15px;
width:65%;
background:linear-gradient(to right,green,orange);
border-radius:10px;
}

.health-score{
font-weight:bold;
}

.suggestions{
margin-top:10px;
font-size:14px;
}

</style>