from flask import Flask, redirect, url_for, request, render_template,session
from flask_socketio import SocketIO, join_room
from collections import OrderedDict
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "Koushik"
socketio = SocketIO(app)
rooms = {}
hosts = []
userRooms = OrderedDict()
drawingUserIds = {}
drawing_coordinates = {}
usernames = {}
userId = 0
arePlaying = []
count = {}
words = {}
wordList = ['cat', 'sun', 'cup', 'ghost', 'flower', 'pie', 'cow', 'banana', 'snowflake', 'bug', 'book', 'jar', 'snake', 'light', 'tree', 'lips', 'apple', 'slide', 'socks', 'smile', 'swing', 'coat', 'shoe', 'water', 'heart', 'hat', 'ocean', 'kite', 'dog', 'mouth', 'milk', 'duck', 'eyes', 'skateboard', 'bird', 'boy', 'apple', 'person', 'girl', 'mouse', 'ball', 'house', 'star', 'nose', 'bed', 'whale', 'jacket', 'shirt', 'hippo', 'beach', 'egg', 'face', 'cookie', 'cheese', 'ice cream cone', 'drum', 'circle', 'spoon', 'worm', 'spider web', 'horse', 'door', 'song', 'trip', 'backbone', 'bomb', 'round', 'treasure', 'garbage', 'park', 'pirate', 'ski', 'state', 'whistle', 'palace', 'baseball', 'coal', 'queen', 'dominoes', 'photograph', 'computer', 'hockey', 'aircraft', 'hot', 'dog', 'salt', 'pepper', 'key', 'iPad', 'whisk', 'frog', 'lawnmower', 'mattress', 'pinwheel', 'cake', 'circus', 'battery', 'mailman', 'cowboy', 'password', 'bicycle', 'skate', 'electricity', 'lightsaber', 'thief', 'teapot', 'deep', 'spring', 'nature', 'shallow', 'toast', 'outside', 'America', 'rollerblading', 'gingerbread', 'man', 'bowtie', 'half', 'spare', 'wax', 'lightbulb', 'platypus', 'music', 'snag', 'jungle', 'important', 'mime', 'peasant', 'baggage', 'hail', 'clog', 'pizza', 'sauce', 'password', 'Heinz', '57', 'scream', 'newsletter', 'bookend', 'pro', 'dripping', 'pharmacist', 'lie', 'catalog', 'ringleader', 'husband', 'laser', 'diagonal', 'comfy', 'myth', 'dorsal', 'biscuit', 'hydrogen', 'macaroni', 'rubber', 'darkness', 'yolk', 'exercise', 'vegetarian', 'shrew', 'chestnut', 'ditch', 'wobble', 'glitter', 'neighborhood', 'dizzy', 'fireside', 'retail', 'drawback', 'logo', 'fabric', 'mirror', 'barber', 'jazz', 'migrate', 'drought', 'commercial', 'dashboard', 'bargain', 'double', 'download', 'professor', 'landscape', 'ski goggles', 'vitamin', 'vision', 'loiterer', 'observatory', 'century', 'Atlantis', 'kilogram', 'neutron', 'stowaway', 'psychologist', 'exponential', 'aristocrat', 'eureka', 'parody', 'cartography', 'figment', 'philosopher', 'tinting', 'overture', 'opaque', 'Everglades', 'ironic', 'zero', 'landfill', 'implode', 'czar', 'armada', 'crisp', 'stockholder', 'inquisition', 'mooch', 'gallop', 'archaeologist', 'blacksmith', 'addendum', 'upgrade', 'hang', 'ten', 'acre', 'twang', 'mine', 'car', 'protestant', 'brunette', 'stout', 'quarantine', 'tutor', 'positive', 'champion', 'pastry', 'tournament', 'rainwater', 'random', 'lyrics', 'ice', 'fishing', 'clue', 'flutter', 'slump', 'ligament', 'flotsam', 'siesta', 'pomp']
scores = {}
indicies = {}
@socketio.on("NextRound")
def nextRound(roomId, userId):
    indicies[roomId] = (indicies[roomId] + 1) % len(rooms[roomId])
    index =indicies[roomId]
    drawingUserIds[roomId] = rooms[roomId][index]
    emitMessageForDrawAlert(roomId,rooms[roomId][index])
    words[roomId] = wordList[random.randint(0,len(wordList)-1)]
    socketio.emit("AssignIds",{"roomId":roomId,"userId":userId, "isDrawing":drawingUserIds[roomId],"isGameOn":roomId in arePlaying, "word":words[roomId]}, to=roomId)
    # socketio.emit("StartGame")

@socketio.on("StartGame1")
def StartGame1(roomId,userId):
    socketio.emit("StartGameFromServer", userId, to=roomId)
@socketio.on("StartGame")
def StartGame(roomId, userId):
    if userId in hosts:
        arePlaying.append(roomId)
        emitMessageForDrawAlert(roomId,userId)
        socketio.emit("StartGameFromServer",userId,to=roomId)

@socketio.on("TimeLeft")
def timeLeft(roomId, time):
    socketio.emit("TimeLeftFromServer",time, to=roomId)

@socketio.on("refresh")
def refresh(roomId):
    socketio.emit("RefreshFromServer",to=roomId)

@socketio.on("StopDrawing")
def stop(roomId):
    socketio.emit("StopDrawingFromServer", to=roomId)
@socketio.on("DrawCurrentPoint")
def DrawFromSocketgrnsjkf(data):
    print("koooooooooooo")
    socketio.emit("DrawCurrentPointFromServer",data,to=data['roomId'])


@socketio.on("EmitMessage")
def emitMessage(message,roomId,userId):
    message = message.lower().strip()
    if message == words[roomId].lower():
        print(userId,"emit message")
        message = usernames[userId] + " won"
        socketio.emit("RemoveScores",to=roomId)
        scores[userId] += 10
        scores[drawingUserIds[roomId]] += 5
        for userIds in rooms[roomId]:
            if userIds in usernames.keys():
                socketio.emit("AddExistingParticipantsForScores", {'username':usernames[userIds],'score':(scores[userIds])},
                              to=roomId)

        socketio.emit("EndGame", (message,drawingUserIds[roomId]), to=roomId)

    elif message == "no one won":
        socketio.emit("EmitMessageFromServer", message, to=roomId)
        socketio.emit("EmitMessageFromServer", "Word is "+ words[roomId], to=roomId)

    elif "won" in message.split(" "):
        socketio.emit("EmitMessageFromServer", message, to=roomId)
        socketio.emit("EmitMessageFromServer", "Word is " + words[roomId], to=roomId)

    else:
        message = usernames[userId]+":"+message
        socketio.emit("EmitMessageFromServer",message,to=roomId)

@socketio.on("EmitMessageForDrawAlert")
def emitMessageForDrawAlert(roomId, userId):
    print(userId,usernames,"emit")
    message = usernames[userId] + " is drawing now"
    socketio.emit("EmitMessageFromServer", message, to=roomId)

@socketio.on("endGame")
def endGame(roomId):
    if roomId not in count.keys():
        count[roomId] = 0
    count[roomId] += 1
    print(count, "count")
    if count[roomId] >= 5:
        socketio.emit("stopGame",to=roomId)

@socketio.on("Join-Rooms")
def joinRooms():
    url = (request.headers['Referer'])
    userId = (url[url.rindex("/") + 1:url.index("?")])
    roomId = (url[url[:url.rindex("/")].rindex("/") + 1:url.rindex("/")])
    lastKey = list(userRooms.keys())[-1] #userId
    join_room(userRooms[lastKey]) #roomId
    socketio.emit("EmitMessageFromServer",usernames[userId]+" has join",to=roomId)
    socketio.emit("AssignIds",{"roomId":userRooms[userId],"userId":lastKey, "isDrawing":drawingUserIds[roomId], "word":words[roomId],"isGameOn":userRooms[userId] in arePlaying}, broadcast=False)
    socketio.emit("RemoveParticipants",to=roomId)
    socketio.emit("RemoveScores",to=roomId)
    for userIds in rooms[roomId]:
        if userIds in usernames.keys():
            socketio.emit("AddExistingParticipants",usernames[userIds],to=roomId)
            socketio.emit("AddExistingParticipantsForScores", {'username':usernames[userIds],'score':(scores[userIds])}, to=roomId)


@app.route("/",methods = ["POST","GET"])
def home():
    if request.method == "POST":
        print(request.form)
    else:
        return render_template("home.html")

@app.route("/room/",methods = ["POST","GET"])
def assignRoom():
    print("request.form,request.values")
    global userId
    if request.method == "POST":
        rId = request.form['roomId']
        if rId in rooms.keys():
            rooms[str(rId)].append(str(userId))
            userId += 1
        else:
            return redirect(url_for("home"))
        return render_template("chat.html", roomId=rId, userId=userId - 1)
    else:
        hosts.append(str(userId))
        rooms[str(len(rooms))] = [str(userId)]
        indicies[str(len(rooms)-1)] = 0
        drawingUserIds[str(len(rooms)-1)] = -1
        userId += 1
        return render_template("chat.html",roomId=len(rooms)-1,userId=userId-1)

@app.route(f'/room/<roomId>/<userId>')
def scrabble(roomId,userId):
    print(request.values)
    usernames[userId] = request.values['username']
    scores[userId] = 0
    if drawingUserIds[roomId] == -1:
        indicies[roomId] = (indicies[roomId]+1) % len(rooms[roomId])
        index = indicies[roomId]
        drawingUserIds[roomId] = rooms[roomId][index]
        words[roomId] = wordList[random.randint(0,len(wordList)-1)]
    userRooms[userId] = roomId
    return render_template("scrabble.html",roomId=roomId)

@socketio.on("ChangeRounds")
def ChangeRounds(roomId):
    print("ChangeRoundsFS")
    socketio.emit("ChangeRoundsFS",to=roomId)

@socketio.on("showScores")
def showScores(roomId):
    s = rooms[roomId]
    s.sort(key=lambda userId:scores[userId])
    st = ""
    for i in s:
        st += usernames[i] + ":" + str(scores[i]) + "\n"
    print("showScores",st)
    socketio.emit("show",st,to=roomId)
@socketio.on("disconnect")
def disconnect():
    url = (request.headers['Referer'])
    userId = (url[url.rindex("/")+1:url.index("?")])
    roomId = (url[url[:url.rindex("/")].rindex("/")+1:url.rindex("/")])
    message = usernames[userId]+" left"
    del usernames[userId]
    del userRooms[userId]
    del scores[userId]
    rooms[roomId].remove(userId)
    if userId in hosts:
        hosts.remove(userId)
        if len(rooms[roomId]) > 0:
            hosts.append(rooms[roomId][0])
    socketio.emit("RemoveParticipants", to=roomId)
    socketio.emit("RemoveScores", to=roomId)
    print(rooms[roomId])
    for userIds in rooms[roomId]:
        if userIds in usernames.keys():
            socketio.emit("AddExistingParticipants", usernames[userIds], to=roomId)
            socketio.emit("AddExistingParticipantsForScores", {'username':usernames[userIds],'score':(scores[userIds])},
                          to=roomId)
    socketio.emit("EmitMessageFromServer", message, to=roomId)


if __name__ == "__main__":
    socketio.run(app)
