from flask import Blueprint, render_template
from flask_login import login_required
from app.models.database import AuditLog, ChatGroup, User
import config

main = Blueprint("main", __name__)

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
    return render_template("users.html", users=config.USERS)
