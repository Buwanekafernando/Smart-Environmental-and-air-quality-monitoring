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
import axios from "axios";

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
text:"Hello! I am your intelligent lab assistant. Ask me about the air quality!"
}
]
}
},
methods:{
toggleChat(){
this.isOpen=!this.isOpen
},
async sendMessage(){
if(!this.userInput) return
const question = this.userInput;
this.messages.push({
id:Date.now(),
type:"user",
text:question
})
this.userInput=""
this.typing=true
try {
  const res = await axios.post("http://localhost:5000/api/chatbot", { message: question });
  this.messages.push({
    id:Date.now()+1,
    type:"bot",
    text:res.data.reply
  });
} catch (error) {
  this.messages.push({
    id:Date.now()+1,
    type:"bot",
    text:"Sorry, I am having trouble connecting to the lab database."
  });
}
this.typing=false
this.$nextTick(() => {
  const container = this.$el.querySelector('.chat-messages');
  if(container) container.scrollTop = container.scrollHeight;
});
}
}
}
</script>

<style scoped>
.chat-toggle {
  position: fixed;
  bottom: 15px;
  right: 15px;
  width: 50px;
  height: 50px;
  background: #2b7cff;
  color: white;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  z-index: 1000;
}
.chat-container {
  position: fixed;
  bottom: 75px;
  right: 15px;
  width: 260px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  overflow: hidden;
  font-family: inherit;
  z-index: 1000;
}
.chat-header {
  background: #2b7cff;
  color: white;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  font-size: 14px;
}
.chat-messages {
  height: 200px;
  overflow-y: auto;
  padding: 8px;
}
.user {
  text-align: right;
  margin: 5px;
  background: #e3f2fd;
  padding: 5px 8px;
  border-radius: 6px;
  font-size: 12px;
  margin-left: 20px;
}
.bot {
  text-align: left;
  margin: 5px;
  background: #f1f1f1;
  padding: 5px 8px;
  border-radius: 6px;
  font-size: 12px;
  margin-right: 20px;
}
.typing {
  font-style: italic;
  color: #888;
}
.chat-input {
  display: flex;
  border-top: 1px solid #edf2f7;
}
.chat-input input {
  flex: 1;
  padding: 8px;
  border: none;
  font-size: 12px;
  outline: none;
}
.chat-input button {
  background: #2b7cff;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 12px;
}
</style>