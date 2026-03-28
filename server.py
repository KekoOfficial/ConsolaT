# 💀 MP SERVER ULTRA STABLE + OPTIMIZED

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import config

# 🚀 APP INIT
app = Flask(__name__)
app.config["SECRET_KEY"] = config.API_TOKEN

socketio = SocketIO(app, cors_allowed_origins="*")

# 📡 HOME
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "server": "MP SYSTEM ACTIVE",
        "host": config.HOST,
        "port": config.PORT
    })

# 🔐 LOGIN SIMPLE
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = data.get("user")
    password = data.get("password")

    if user == config.ADMIN_USER and password == config.ADMIN_PASS:
        return jsonify({"status": "success", "token": config.API_TOKEN})

    return jsonify({"status": "error", "message": "invalid credentials"}), 401

# 💬 SOCKET CONNECT
@socketio.on("connect")
def connect():
    emit("status", {"message": "connected to MP system"})

# 💬 CHAT MESSAGE
@socketio.on("message")
def handle_message(data):
    print("MSG:", data)
    emit("message", data, broadcast=True)

# 📊 USERS LIST
@app.route("/users")
def users():
    return jsonify(config.USERS)

# 💀 GROUPS
@app.route("/groups")
def groups():
    return jsonify(config.GROUPS)

# ⚡ RUN SERVER
if __name__ == "__main__":
    print("💀 MP SERVER STARTING...")
    print(f"HOST: {config.HOST}")
    print(f"PORT: {config.PORT}")

    socketio.run(
        app,
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )