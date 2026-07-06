from app import socketio
from flask_socketio import emit
from app.services.telegram import TelegramService
from app.models.database import db, AuditLog, Message
from datetime import datetime

@socketio.on("connect")
def handle_connect():
    emit("status", {"message": "Conectado al Gateway Empresarial"})

@socketio.on("message")
def handle_message(data):
    chat_id = data.get("chat_id")
    text = data.get("text")
    sender = data.get("sender", "System")

    # Registro en Auditoría
    log_msg = f"Mensaje de {sender} para {chat_id}: {text[:50]}..."
    from flask import current_app
    with current_app.app_context():
        new_log = AuditLog(event=log_msg)
        db.session.add(new_log)

        # Guardar mensaje
        new_msg = Message(chat_id=chat_id, text=text, sender=sender)
        db.session.add(new_msg)
        db.session.commit()

        # Enviar a Telegram
        res = TelegramService.send_message(chat_id, text)

        # Notificar a otros clientes
        data["time"] = datetime.now().strftime("%H:%M:%S")
        emit("message", data, broadcast=True)

        # Emitir log a la interfaz
        emit("log", {"time": data["time"], "msg": log_msg}, broadcast=True)
