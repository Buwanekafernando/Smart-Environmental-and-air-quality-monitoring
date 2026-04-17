<template>

<div class="alert-box" v-if="coAnalysis && coAnalysis.smoking_detected">

<h2>🚨 Smoke/High CO Alert</h2>

<p>Abnormal CO level spikes detected! Possible smoking or fire hazard.</p>

<div class="recommend">
Recommendation: Please open windows for better ventilation and check the premises immediately.
</div>

</div>

</template>

<script>
export default {
  props: {
    coAnalysis: {
      type: Object,
      default: null
    }
  }
}
</script>

<style>

.alert-box{
background:#f8e7e7;
border:2px solid red;
padding:20px;
border-radius:10px;
margin-bottom:30px;
/* Add a pulsing animation to alert */
animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
}

.recommend{
background:white;
padding:10px;
border-radius:8px;
margin-top:10px;
}

</style>