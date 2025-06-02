import os
import json
import time
from flask import Blueprint, request, jsonify

bp = Blueprint("watch_add", __name__)
SESSION_FILE = "watch_sessions.json"

def load_sessions():
    if not os.path.exists(SESSION_FILE):
        return {}
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_sessions(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_watch_id(session_data):
    count = 1
    while True:
        key = f"watch_{count:03d}"
        if key not in session_data:
            return key
        count += 1

@bp.post("/watch_add")
def add_watch():
    data = request.get_json()
    print(data)
    required_fields = ["sessionId", "camera_id", "address", "watchTime"]
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    session_id = data["sessionId"]
    sessions = load_sessions()

    if session_id not in sessions:
        sessions[session_id] = {}

    session_data = sessions[session_id]
    watch_id = get_next_watch_id(session_data)

    session_data[watch_id] = {
        "camera_id": data["camera_id"],
        "address": data["address"],
        "watchTime": data["watchTime"],
        "startTime": int(time.time()),
        "status": "unknown",
        "notified": False
    }

    save_sessions(sessions)

    return jsonify({
        "message": "Watch added",
        "watchId": watch_id,
        "session data" : session_data
    }), 200
