from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from routes.watch_camera import get_watched_cameras

app = Flask(__name__)
CORS(app)

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == "__main__":
    print("Starting WebSocket server on http://0.0.0.0:8001")
    socketio.run(app, host="0.0.0.0", port=8001) 