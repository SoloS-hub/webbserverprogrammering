from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

chat_logger = setup_logger('chat_logger', 'chat.log')
chat_logger.info('This is just info message')

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
