<template>

<div class="health-card">

<h2>Room Health & Insights</h2>

<div class="health-grid">

<!-- Left side -->
<div class="people-card">

<h4>Any people in the Room?</h4>

<div class="people-chart">
✔
<p>Human Presence Detected</p>
</div>

</div>

<!-- Right side -->
<div class="health-info">

<p>
Motion sensor has detected 2 people in the room.
Air quality monitoring is adjusted based on occupancy.
</p>

<div class="health-bar">

<div class="health-fill"></div>

</div>

<p class="health-score">65% Healthy</p>

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