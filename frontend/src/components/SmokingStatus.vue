<template>

<div class="smoke-section">

<div class="smoke-card smoking">

<h3>🚨 Someone Smoking</h3>

<p>Alert Triggered</p>

</div>

<div class="smoke-card safe">

<h3>🙂 Not Smoking</h3>

<p>All Clear</p>

</div>

</div>

</template>

<style>

.smoke-section{
display:grid;
grid-template-columns:1fr 1fr;
gap:20px;
margin-top:30px;
}

.smoke-card{
padding:25px;
border-radius:15px;
text-align:center;
font-size:18px;
}

.smoking{
background:#ffe6ea;
border:2px solid #ff4b6e;
color:#ff4b6e;
}

.safe{
background:#f5f5f5;
color:#888;
}

</style>