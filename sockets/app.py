from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on("connect")
def handel_conect():
    print(f"User has conected: {request.sid}")
    emit("user_connected", broadcast=True)

@socketio.on("message")
def message(message):
    print(f"User: {request.sid} has sent a message")
    emit("message", broadcast=True)
    


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
