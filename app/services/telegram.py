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

    @staticmethod
    def set_webhook(url):
        webhook_url = f"https://api.telegram.org/bot{config.API_TOKEN}/setWebhook"
        payload = {"url": url}
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def parse_update(data):
        """
        Parses a Telegram update and returns a simplified dictionary.
        """
        if "message" in data:
            message = data["message"]
            return {
                "type": "message",
                "chat_id": str(message["chat"]["id"]),
                "text": message.get("text", ""),
                "sender": message["from"].get("username") or message["from"].get("first_name") or "Unknown",
                "date": message.get("date")
            }
        return None
