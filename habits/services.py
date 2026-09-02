import requests
from django.conf import settings


def send_telegram_message(telegram_chat_id: int, message: str) -> None:
    """Отправляет текстовое сообщение в Telegram-чат через Bot API."""
    token = settings.TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {"chat_id": telegram_chat_id, "text": message}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
