from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room

chatlog = []

users = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    join_room(username)
    emit("message", f"{username} joined the chat", broadcast=True)

@socketio.on("message")
def message(message):
    print(f"User: {users[request.sid]} has sent a message : {message}")
    emit("message", f"{users[request.sid]} sent: {message}", broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
