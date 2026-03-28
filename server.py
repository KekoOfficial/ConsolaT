import asyncio
import os
import threading
from flask import Flask, request, jsonify, render_template

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

from config import TOKEN, LOG_FILE, WEB_HOST, WEB_PORT

app = Flask(__name__)

tg_app = Application.builder().token(TOKEN).build()

# =========================
# 📂 LOGS
# =========================

def save_log(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def load_logs():
    if os.path.exists(LOG_FILE):
        return open(LOG_FILE, encoding="utf-8").readlines()[-50:]
    return []

# =========================
# 🤖 MENSAJES RECIBIDOS
# =========================

async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    chat = update.effective_chat
    msg = update.message.text

    line = f"📩 {user.id}|{chat.id}|{user.first_name}: {msg}"

    print(line)
    save_log(line)

tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir))

# =========================
# 📡 ENVIAR MENSAJE (FIX ESTABLE)
# =========================

async def send_async(data):
    try:
        await tg_app.bot.send_message(
            chat_id=int(data["id"]),
            text=data["msg"]
        )

        line = f"🤖 BOT -> {data['id']}: {data['msg']}"
        print(line)
        save_log(line)

        # 💀 CC OPCIONAL
        if data.get("cc"):
            await tg_app.bot.send_message(
                chat_id=int(data["cc"]),
                text=data["msg"]
            )

            line2 = f"🤖 BOT CC -> {data['cc']}: {data['msg']}"
            print(line2)
            save_log(line2)

    except Exception as e:
        print("❌ ERROR SEND:", e)

@app.route("/send", methods=["POST"])
def send():
    data = request.json

    # 🔥 FIX IMPORTANTE: thread (NO rompe Flask)
    threading.Thread(target=lambda: asyncio.run(send_async(data))).start()

    return jsonify({"status": "ok"})

# =========================
# 🌐 PÁGINAS
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
# 🌐 FLASK
# =========================

def run_web():
    app.run(host=WEB_HOST, port=WEB_PORT, debug=False)

# =========================
# 🚀 MAIN
# =========================

async def main():
    threading.Thread(target=run_web).start()
    await bot_run()

if __name__ == "__main__":
    asyncio.run(main())