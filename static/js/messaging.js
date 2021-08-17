socket.on("EmitMessageFromServer",message=>{
    addMessageToContainer(message)
})
function sendMessage(){
    event.preventDefault()
    let val = document.getElementById("msg").value
    document.getElementById("msg").value = ""
    socket.emit("EmitMessage",val,roomId,id)
}

function addMessageToContainer(message){
    console.log(message,"Chst")
    let msg = document.createElement("div")
    let sender = document.createElement("div")
    let msg_content = document.createElement("div")

    msg.className = "msg"
    sender.className = "sender"
    msg_content.className = "msg_content"
    if(message.indexOf(":") >= 0){
        words = message.split(":");
        sender.innerHTML = words[0]
        msg_content.innerHTML = words[1]
    }
    else msg_content.innerHTML = message
    msg.appendChild(sender)
    msg.appendChild(msg_content)
    document.getElementById("chat-container").appendChild(msg)
}

