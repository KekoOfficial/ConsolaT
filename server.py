import asyncio
import os
import json
import uuid
import threading

from flask import Flask, request, jsonify, render_template, send_from_directory

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

from config import *

# =========================
# 🌐 APP
# =========================

app = Flask(__name__, template_folder="templates")

tg_app = Application.builder().token(TOKEN).build()

# =========================
# 📂 SETUP
# =========================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# 📂 LOGS
# =========================

def save_log(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def load_logs():
    if os.path.exists(LOG_FILE):
        return open(LOG_FILE, encoding="utf-8").readlines()[-100:]
    return []

# =========================
# 💬 CHATS
# =========================

def load_chats():
    if os.path.exists(CHATS_FILE):
        return json.load(open(CHATS_FILE))
    return {}

def save_chat(chat_id, name):
    chats = load_chats()
    chats[str(chat_id)] = name
    json.dump(chats, open(CHATS_FILE, "w"))

# =========================
# 🤖 RECIBIR MENSAJES
# =========================

async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    chat = update.effective_chat

    name = user.first_name if user else "Grupo"
    msg = ""

    # TEXTO
    if update.message.text:
        msg = update.message.text

    # FOTO
    elif update.message.photo:
        file = await update.message.photo[-1].get_file()
        msg = f"[FOTO] {file.file_path}"

    # VIDEO
    elif update.message.video:
        file = await update.message.video.get_file()
        msg = f"[VIDEO] {file.file_path}"

    # VOZ
    elif update.message.voice:
        file = await update.message.voice.get_file()
        msg = f"[VOZ] {file.file_path}"

    # AUDIO
    elif update.message.audio:
        file = await update.message.audio.get_file()
        msg = f"[AUDIO] {file.file_path}"

    line = f"{chat.id}|{name}: {msg}"

    print(line)
    save_log(line)
    save_chat(chat.id, name)

tg_app.add_handler(MessageHandler(filters.ALL, recibir))

# =========================
# 📡 ENVIAR
# =========================

async def send_async(data):
    try:
        chat_id = int(data["id"])

        # TEXTO
        if data.get("msg"):
            await tg_app.bot.send_message(chat_id=chat_id, text=data["msg"])

        # ARCHIVO
        if data.get("file"):
            url = BASE_URL + data["file"]

            if url.endswith((".jpg",".png",".jpeg")):
                await tg_app.bot.send_photo(chat_id=chat_id, photo=url)

            elif url.endswith(".mp4"):
                await tg_app.bot.send_video(chat_id=chat_id, video=url)

        print(f"🤖 enviado a {chat_id}")

    except Exception as e:
        print("❌ ERROR:", e)

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    threading.Thread(target=lambda: asyncio.run(send_async(data))).start()
    return jsonify({"status": "ok"})

# =========================
# 📤 SUBIR ARCHIVOS
# =========================

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return {"error": "no file"}

    name = str(uuid.uuid4()) + "_" + file.filename
    path = os.path.join(UPLOAD_FOLDER, name)

    file.save(path)

    return {"url": f"/file/{name}"}

@app.route("/file/<name>")
def file(name):
    return send_from_directory(UPLOAD_FOLDER, name)

# =========================
# 🌐 WEB
# =========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/grupo")
def grupo():
    return render_template("grupo.html")

@app.route("/logs")
def logs():
    return jsonify({"logs": load_logs()})

@app.route("/chats")
def chats():
    return jsonify(load_chats())

# =========================
# 🤖 BOT LOOP
# =========================

async def bot_run():
    await tg_app.initialize()
    await tg_app.start()

    await tg_app.bot.delete_webhook(drop_pending_updates=True)
    await tg_app.updater.start_polling()

    print("🤖 BOT ONLINE")

    while True:
        await asyncio.sleep(10)

# =========================
# 🚀 MAIN
# =========================

def run_web():
    app.run(host=WEB_HOST, port=WEB_PORT, debug=False)

async def main():
    threading.Thread(target=run_web).start()
    await bot_run()

if __name__ == "__main__":
    asyncio.run(main())