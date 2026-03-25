<template>

<!-- Floating Button -->
<div class="chat-toggle" @click="toggleChat">
💬
</div>

<!-- Chat Window -->
<div v-if="isOpen" class="chat-container">

<div class="chat-header">
AI Assistant
</div>

<div class="chat-messages">

<div v-for="msg in messages" :key="msg.id" :class="msg.type">
{{msg.text}}
</div>

<div v-if="typing" class="bot typing">
AI is typing...
</div>

</div>

<div class="chat-input">

<input
v-model="userInput"
placeholder="Ask about the dashboard..."
@keyup.enter="sendMessage"
/>

<button @click="sendMessage">Send</button>

</div>

</div>

</template>

<script>

export default{

data(){
return{

isOpen:false,
typing:false,
userInput:"",

messages:[
{
id:1,
type:"bot",
text:"Hello! I can help explain the environmental data."
}
]

}
},

methods:{

toggleChat(){
this.isOpen=!this.isOpen
},

sendMessage(){

if(!this.userInput) return

this.messages.push({
id:Date.now(),
type:"user",
text:this.userInput
})

this.typing=true

const question=this.userInput.toLowerCase()

setTimeout(()=>{

let reply=""

if(question.includes("air"))
reply="The current air quality indicates moderate pollution."

else if(question.includes("temperature"))
reply="The room temperature is around 27°C."

else if(question.includes("people"))
reply="The PIR sensor indicates human presence in the room."

else if(question.includes("smoke"))
reply="Smoking activity was detected earlier."

else
reply="I'm analyzing the environmental dashboard."

this.messages.push({
id:Date.now()+1,
type:"bot",
text:reply
})

this.typing=false

},1000)

this.userInput=""

}

}

}

</script>

<style>

.chat-toggle{
position:fixed;
bottom:20px;
right:20px;
width:60px;
height:60px;
background:#2b7cff;
color:white;
font-size:25px;
display:flex;
align-items:center;
justify-content:center;
border-radius:50%;
cursor:pointer;
box-shadow:0 5px 20px rgba(0,0,0,0.3);
}

.chat-container{
position:fixed;
bottom:90px;
right:20px;
width:300px;
background:white;
border-radius:12px;
box-shadow:0 10px 25px rgba(0,0,0,0.2);
overflow:hidden;
font-family:Arial;
}

.chat-header{
background:#2b7cff;
color:white;
padding:12px;
text-align:center;
font-weight:bold;
}

.chat-messages{
height:220px;
overflow-y:auto;
padding:10px;
}

.user{
text-align:right;
margin:6px;
background:#e3f2fd;
padding:6px;
border-radius:6px;
}

.bot{
text-align:left;
margin:6px;
background:#f1f1f1;
padding:6px;
border-radius:6px;
}

.typing{
font-style:italic;
color:#888;
}

.chat-input{
display:flex;
border-top:1px solid #ddd;
}

.chat-input input{
flex:1;
padding:8px;
border:none;
}

.chat-input button{
background:#2b7cff;
color:white;
border:none;
padding:8px 12px;
cursor:pointer;
}

</style>