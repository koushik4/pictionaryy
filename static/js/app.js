var socket = io();
var id = -1
var roomId = -1
var lineWidth = 5
var startx = -1, starty = -1, endx = -1, endy = -1, prevx = -1, prevy = -1;
var eraserSize = 35
var color = 'black'
var time = 0
var timerFunction = -1
var word = ""
var canvas = document.getElementById("canvas")
var draw = canvas.getContext("2d")
var isDrawing = false
var isGameOn = false
var rounds = 5
document.getElementById("bgm").volume = 0.1

canvas.height = window.innerHeight
canvas.width = window.innerWidth
draw.beginPath()

draw.lineCap = 'round';
draw.lineWidth = lineWidth;

var isEraser = false
var canDraw = false
var isMouseDown = false
var lineColor = "black"
console.log("hellooo")
socket.emit("Join-Rooms")

socket.on("RemoveParticipants",()=>{
    let body = document.getElementById("participants").childNodes
    while(body.length != 0)body[0].remove()
})

socket.on("RemoveScores",()=>{
    let body = document.getElementById("score").childNodes
    while(body.length != 0)body[0].remove()
})

socket.on("AddExistingParticipants",username=>{
    var p = document.createElement("p")
    console.log("scor1")
    p.innerHTML = username
    document.getElementById("participants").appendChild(p)
})
socket.on("AddExistingParticipantsForScores",username=>{
    console.log("score")
    var p = document.createElement("p")
    p.innerHTML = username
    document.getElementById("score").appendChild(p)
})
socket.on("StartGameFromServer",(userId)=>{
    isGameOn = true
})
socket.on("TimeLeftFromServer",time=>{
    document.getElementById("time").innerHTML = "Time Left:" + (120-time)
})
socket.on("DrawCurrentPointFromServer",obj=>{
    draw.strokeStyle = obj['color'];
    draw.lineWidth = obj['width']
    console.log("Drawing")
    draw.lineTo(obj['x'], obj['y']);
    draw.stroke();
    draw.strokeStyle = color;
})

socket.on("StopDrawingFromServer",()=>{
    draw.beginPath();
})

socket.on("RefreshFromServer",()=>{
    draw.fillStyle = "white";
    draw.fillRect(0, 0, canvas.width, canvas.height);
})

function changeColor(col){
    console.log(col)
    draw.strokeStyle = col
    color = col
}
socket.on("EndGame",(message, userId)=>{
    console.log(message,userId,"end game")
    document.getElementById("win").play()
    if(id!=userId)return
    console.log(id)
    clearInterval(timerFunction)
    endGame(message)
})

socket.on("stopGame",()=>{
    isGameOn = false;
})
socket.on("ChangeRoundsFS",()=>{
    rounds -= 1
    document.getElementById("round").innerHTML = "Round: "+rounds

})
function KeepDrawing(){
    if(!isDrawing)return
    isMouseDown = true  
}

function StopDrawing(){
    if(!isDrawing || !isGameOn)return
    isMouseDown = false
    draw.beginPath();
    socket.emit("StopDrawing",roomId)
}

function eraser(){
    if(!isDrawing || !isGameOn)return
    isEraser = true
}

function refresh(){
    if(!isDrawing|| !isGameOn)return
    isEraser = false
    draw.fillStyle = "white";
    draw.fillRect(0, 0, canvas.width, canvas.height);
    socket.emit("refresh",roomId)
}

function DrawOnCanvas(){
    if(isMouseDown && !isEraser && isDrawing && isGameOn) {
        draw.strokeStyle = color;
        var rect = canvas.getBoundingClientRect();
        var scaleX = canvas.width / rect.width;
        var scaleY = canvas.height / rect.height;
        let x = (event.clientX - rect.left) * scaleX;
        let y = (event.clientY - rect.top) * scaleY;
        let data = {'x':x,'y':y,'width':lineWidth, 'color':color,'roomId':roomId}
        draw.lineTo(x, y);
        draw.stroke();
        socket.emit('DrawCurrentPoint',data)
    }
    if(isMouseDown && isEraser && isDrawing && isGameOn) {
        draw.fillStyle = "white";
        var rect = canvas.getBoundingClientRect();
        var scaleX = canvas.width / rect.width;
        var scaleY = canvas.height / rect.height;
        let x = (event.clientX - rect.left) * scaleX;
        let y = (event.clientY - rect.top) * scaleY;
        draw.fillRect(x, y, eraserSize, eraserSize);
    }
}
function changeSize(width){
    isEraser = false
    lineWidth = width
    draw.lineWidth = width
}

function Timer(){
    if(!isDrawing || !isGameOn)return;
    time+=1
    document.getElementById("word").innerHTML = "Your word is:"+ word
    socket.emit("TimeLeft",roomId,time)
    if(time >= 120){
        clearInterval(timerFunction)
        endGame("No one won")
    }
}


function startgame(){
    console.log("start game")
    socket.emit("StartGame",roomId,id)
}
function timeEvent(){
      console.log("love")
      socket.emit("NextRound",roomId,id)
      if(isDrawing){
         socket.emit("StartGame1",roomId,id)
      }
}

function endGame(message){
    console.log(isDrawing,"endgame")
    isDrawing = false
    time = 0
    clearInterval(timerFunction)
    refresh()
    timerFunction = -1
    document.getElementById("word").innerHTML = ""
    socket.emit("EmitMessage",message,roomId,id)
    socket.emit("endGame",roomId)
    console.log(rounds)
    if(rounds > 1){
        document.getElementById("next").click()
        socket.emit("ChangeRounds",roomId)
    }
    else{
        socket.emit("showScores",roomId)
        rounds = 0
        time = 0
        color = 'black'
    }
}
function mute(){
    console.log("mutee")
    if(document.getElementById("bgm").volume != 0.0){
        document.getElementById("bgm").volume = 0.0
        document.getElementById("mute").innerHTML = "unmute"
    }
    else{
        document.getElementById("bgm").volume = 0.1
        document.getElementById("mute").innerHTML = "mute"
    }
}
socket.on("show",s=>{
    var p = document.createElement("p")
    p.innerHTML = s
    document.getElementById("reward").appendChild(p)
})
socket.on("AssignIds",data=>{
    if(id < 0 && roomId < 0){
        id = data['userId']
        roomId = data['roomId']
        console.log(data['isDrawing'])
    }
    if(id==data['isDrawing']){
            isDrawing=true
            console.log(id,data,isDrawing,timerFunction)
            if(timerFunction == -1)
            timerFunction = setInterval(Timer,1000)
            word = data['word']
    }
    isGameOn = data['isGameOn']

})
