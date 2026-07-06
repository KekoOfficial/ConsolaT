# 💀 MP SERVER ULTRA STABLE + OPTIMIZED

from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit
from functools import wraps
from datetime import datetime
import requests
import config

# 🚀 APP INIT
app = Flask(__name__)
app.config["SECRET_KEY"] = config.API_TOKEN # Usando token como secret key única

socketio = SocketIO(app, cors_allowed_origins="*")

# 📝 LOGS STORAGE
SYSTEM_LOGS = []

def add_log(msg):
    time_str = datetime.now().strftime("%H:%M:%S")
    log_entry = {"time": time_str, "msg": msg}
    SYSTEM_LOGS.insert(0, log_entry)
    if len(SYSTEM_LOGS) > config.MAX_LOGS:
        SYSTEM_LOGS.pop()
    socketio.emit("log", log_entry)

# 🔐 AUTH DECORATOR
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function

# 🏠 ROUTES
@app.route("/")
@login_required
def index():
    return render_template("index.html", users=config.USERS)

@app.route("/login")
def login_page():
    if "logged_in" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        users_count=len(config.USERS),
        groups_count=len(config.GROUPS),
        host=config.HOST,
        port=config.PORT
    )

@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")

@app.route("/grupo")
@login_required
def grupo():
    return render_template("grupo.html", groups=config.GROUPS)

@app.route("/logs")
@login_required
def logs_page():
    return render_template("logs.html", logs=SYSTEM_LOGS)

@app.route("/media")
@login_required
def media():
    return render_template("media.html")

@app.route("/send")
@login_required
def send():
    return render_template("send.html")

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", config=config)

@app.route("/users_list")
@login_required
def users_list():
    return render_template("users.html", users=config.USERS)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login_page"))

# 🔐 LOGIN API
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    user = data.get("user")
    password = data.get("password")

    if user == config.ADMIN_USER and password == config.ADMIN_PASS:
        session["logged_in"] = True
        add_log(f"Acceso exitoso: {user}")
        return jsonify({"status": "success", "token": config.API_TOKEN})

    add_log(f"Intento de acceso fallido: {user}")
    return jsonify({"status": "error", "message": "invalid credentials"}), 401

# 📊 DATA API
@app.route("/api/users")
@login_required
def api_users():
    return jsonify(config.USERS)

@app.route("/api/groups")
@login_required
def api_groups():
    return jsonify(config.GROUPS)

# 🤖 TELEGRAM BOT
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{config.API_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return {"ok": False, "error": str(e)}

# 💬 SOCKET CONNECT
@socketio.on("connect")
def connect():
    emit("status", {"message": "connected to MP system"})

# 💬 CHAT MESSAGE
@socketio.on("message")
def handle_message(data):
    chat_id = data.get("chat_id")
    text = data.get("text")
    sender = data.get("sender", "Unknown")

    add_log(f"Mensaje de {sender} para {chat_id}: {text}")

    if chat_id and text:
        # Intentar enviar a Telegram
        res = send_telegram_message(chat_id, text)
        data["telegram_status"] = res.get("ok", False)
        if not data["telegram_status"]:
            add_log(f"Error Telegram: {res.get('description', 'Error desconocido')}")

    emit("message", data, broadcast=True)

@socketio.on("update")
def handle_update(data):
    emit("update", data, broadcast=True)

# ⚡ RUN SERVER
if __name__ == "__main__":
    print("💀 MP SERVER STARTING...")
    print(f"HOST: {config.HOST}")
    print(f"PORT: {config.PORT}")

    # Log de inicio
    add_log("Sistema iniciado y listo.")

    socketio.run(
        app,
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
