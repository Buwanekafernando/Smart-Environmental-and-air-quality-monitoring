<template>

<div class="card">

<h3>🌡 Room Temperature</h3>

<div class="temp-icon">🌡</div>

<div class="temp-value">
{{temperature}}°C
</div>

<p>This is your room Temp</p>

</div>

</template>

<script>

export default{

data(){
return{
temperature:27
}
},

mounted(){

setInterval(()=>{

// simulate sensor value
this.temperature = 25 + Math.floor(Math.random()*5)

},4000)

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

.temp-icon{
font-size:60px;
margin:10px 0;
}

.temp-value{
font-size:40px;
color:red;
margin:10px 0;
}

</style>