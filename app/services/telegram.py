import requests
import config

class TelegramService:
    @staticmethod
    def send_message(chat_id, text):
        url = f"https://api.telegram.org/bot{config.API_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}
