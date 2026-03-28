from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import time
from config import config

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=config.socket.cors)

# 💾 MEMORY FAST
private_chats = {}
logs = []


# 🔐 AUTH CHECK
def auth():
    return request.headers.get("Authorization") == config.auth.api_token


# 📜 LOG SYSTEM
def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    logs.append(line)
    socketio.emit("log", line)


# =========================
# 💬 PRIVATE CHAT
# =========================
@app.route("/api/private/send", methods=["POST"])
def private_send():

    if not auth():
        return jsonify({"error": "unauthorized"}), 403

    data = request.json
    sender = data["from"]
    to = data["to"]
    msg = data["message"]

    chat_id = f"{min(sender,to)}-{max(sender,to)}"

    if chat_id not in private_chats:
        private_chats[chat_id] = []

    message = {
        "from": sender,
        "to": to,
        "message": msg,
        "time": time.strftime("%H:%M:%S")
    }

    private_chats[chat_id].append(message)

    log(f"PM {sender}->{to}: {msg}")

    socketio.emit("private_message", message)

    return jsonify({"status": "ok", "data": message})


# =========================
# 💬 GROUP CHAT
# =========================
@app.route("/api/group/send", methods=["POST"])
def group_send():

    if not auth():
        return jsonify({"error": "unauthorized"}), 403

    data = request.json
    group_id = data["group_id"]
    sender = data["from"]
    msg = data["message"]

    message = {
        "from": sender,
        "message": msg,
        "time": time.strftime("%H:%M:%S")
    }

    config.groups.groups[group_id]["messages"].append(message)

    log(f"GROUP {group_id} {sender}: {msg}")

    socketio.emit("group_message", {
        "group_id": group_id,
        "data": message
    })

    return jsonify({"status": "ok", "data": message})


# =========================
# 👤 USERS
# =========================
@app.route("/api/users")
def users():
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(config.users.users)


# =========================
# 💬 GROUPS
# =========================
@app.route("/api/groups")
def groups():
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(config.groups.groups)


# =========================
# 📜 LOGS
# =========================
@app.route("/api/logs")
def get_logs():
    if not auth():
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(logs[-100:])


# =========================
# 🔐 LOGIN
# =========================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    if data["user"] == config.auth.admin_user and data["password"] == config.auth.admin_pass:
        return jsonify({
            "status": "ok",
            "token": config.auth.api_token
        })

    return jsonify({"status": "error"}), 401


# =========================
# 🔌 SOCKET EVENTS
# =========================
@socketio.on("connect")
def connect():
    log("USER CONNECTED")
    emit("status", {"msg": "connected"})


@socketio.on("send_message")
def socket_msg(data):
    log(f"SOCKET: {data}")
    emit("message", data, broadcast=True)


# =========================
# 🚀 START SERVER
# =========================
if __name__ == "__main__":
    socketio.run(
        app,
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug
    )