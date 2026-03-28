from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import time
import config

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=config.SOCKET_CORS)

# 💾 MEMORY SYSTEM (FAST ACCESS)
users = config.USERS
groups = config.GROUPS
private_chats = {}
logs = []


# ⚡ UTIL: TOKEN CHECK (FAST)
def auth():
    return request.headers.get("Authorization") == config.API_TOKEN


# 📜 ULTRA LOG SYSTEM
def log(msg):
    data = f"[{time.strftime('%H:%M:%S')}] {msg}"
    logs.append(data)
    socketio.emit("log", data)


# 💬 PRIVATE CHAT (ULTRA FAST)
@app.route("/api/private/send", methods=["POST"])
def private_send():

    if not auth():
        return jsonify({"error": "unauthorized"}), 403

    d = request.json
    sender = d["from"]
    to = d["to"]
    msg = d["message"]

    chat_id = f"{min(sender,to)}-{max(sender,to)}"

    if chat_id not in private_chats:
        private_chats[chat_id] = []

    data = {
        "from": sender,
        "to": to,
        "message": msg,
        "time": time.strftime("%H:%M:%S")
    }

    private_chats[chat_id].append(data)

    log(f"PM {sender}->{to}: {msg}")

    socketio.emit("private_message", data)

    return jsonify({"status": "ok", "data": data})


# 💬 GROUP CHAT (FAST PUSH)
@app.route("/api/group/send", methods=["POST"])
def group_send():

    if not auth():
        return jsonify({"error": "unauthorized"}), 403

    d = request.json
    group_id = d["group_id"]
    sender = d["from"]
    msg = d["message"]

    data = {
        "from": sender,
        "message": msg,
        "time": time.strftime("%H:%M:%S")
    }

    groups[group_id]["messages"].append(data)

    log(f"GROUP {group_id} {sender}: {msg}")

    socketio.emit("group_message", {
        "group_id": group_id,
        "data": data
    })

    return jsonify({"status": "ok", "data": data})


# 👤 USERS
@app.route("/api/users")
def get_users():
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(users)


# 💬 GROUPS
@app.route("/api/groups")
def get_groups():
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(groups)


# 📜 LOGS (MP CONTROL CENTER)
@app.route("/api/logs")
def get_logs():
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(logs[-100:])  # solo últimos 100 (rápido)


# 💬 PRIVATE HISTORY
@app.route("/api/private/<chat_id>")
def private_history(chat_id):
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(private_chats.get(chat_id, []))


# 🔐 LOGIN ADMIN
@app.route("/api/login", methods=["POST"])
def login():
    d = request.json

    if d["user"] == config.ADMIN_USER and d["password"] == config.ADMIN_PASS:
        return jsonify({"status": "ok", "token": config.API_TOKEN})

    return jsonify({"status": "error"}), 401


# 🔌 SOCKET CONNECT
@socketio.on("connect")
def connect():
    log("USER CONNECTED")
    emit("status", {"msg": "connected"})


# 🔌 SOCKET MESSAGE (GLOBAL REALTIME)
@socketio.on("send_message")
def socket_msg(data):
    log(f"SOCKET MSG: {data}")
    emit("message", data, broadcast=True)


# 🚀 START SERVER (FAST MODE)
if __name__ == "__main__":
    socketio.run(
        app,
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        allow_unsafe_werkzeug=True
    )