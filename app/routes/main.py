from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.models.database import db, AuditLog, ChatGroup, User, Message
from app import socketio
import config
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Log the update for debugging
    # print(f"Received update: {data}")

    if "message" in data:
        message = data["message"]
        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")
        sender = message["from"].get("username") or message["from"].get("first_name") or "Unknown"

        # Save to DB
        new_msg = Message(chat_id=chat_id, text=text, sender=sender)
        db.session.add(new_msg)

        log_entry = AuditLog(event=f"Webhook: Mensaje recibido de {sender} en {chat_id}: {text[:50]}")
        db.session.add(log_entry)
        db.session.commit()

        # Emit via Socket.IO
        socketio.emit("message", {
            "chat_id": chat_id,
            "text": text,
            "sender": sender,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        socketio.emit("log", {
            "time": datetime.now().strftime("%H:%M:%S"),
            "msg": f"Entrante: {sender}: {text[:50]}"
        })

    return jsonify({"status": "ok"}), 200

@main.route("/")
@login_required
def index():
    return render_template("index.html", users=config.USERS)

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        users_count=User.query.count(),
        groups_count=len(config.GROUPS),
        host=config.HOST,
        port=config.PORT
    )

@main.route("/logs")
@login_required
def logs():
    logs_data = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return render_template("logs.html", logs=logs_data)

@main.route("/chat")
@login_required
def chat():
    return render_template("chat.html")

@main.route("/grupo")
@login_required
def grupo():
    return render_template("grupo.html", groups=config.GROUPS)

@main.route("/settings")
@login_required
def settings():
    return render_template("settings.html", config=config)

@main.route("/users_list")
@login_required
def users_list():
    # Show both config users (hardcoded) and database users (admins)
    db_users = User.query.all()
    return render_template("users.html", users=config.USERS, db_users=db_users)
