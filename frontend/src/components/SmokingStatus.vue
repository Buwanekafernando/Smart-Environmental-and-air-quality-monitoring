<template>

<div class="smoke-section">

<div class="smoke-card smoking" v-if="motion === 1">

<h3>🚨 Presence: Detected</h3>

<p>Motion in Room</p>

</div>

<div class="smoke-card safe" v-else>

<h3>🙂 Presence: Not Detected</h3>

<p>No Motion Detected</p>

</div>

</div>

</template>

<script>
export default {
  props: {
    motion: {
      type: Number,
      default: 0
    }
  }
}
</script>

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