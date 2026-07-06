import requests
import time

def test_webhook():
    print("Testing Webhook...")
    webhook_url = "http://localhost:5000/webhook"
    payload = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 987654321,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 987654321,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1625562238,
            "text": "Hola desde Telegram Simulator"
        }
    }

    try:
        response = requests.post(webhook_url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Start the app in the background first if not running
    # For testing purposes, we assume the user can run the app or we run a mock check
    test_webhook()
