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
    let msg = document.createElement("p")
    msg.innerHTML = message
    document.getElementById("chat-container").appendChild(msg)
}

