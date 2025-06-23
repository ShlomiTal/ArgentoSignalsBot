import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text, chat_id=None, parse_mode="Markdown"):
    chat_id = chat_id or CHAT_ID
    if not TELEGRAM_TOKEN or not chat_id:
        print("[Telegram] Missing token or chat_id")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }

    try:
        res = requests.post(url, data=data)
        return res.status_code == 200
    except Exception as e:
        print("[Telegram Error]", e)
        return False

def send_photo(image_path, caption="", chat_id=None):
    chat_id = chat_id or CHAT_ID
    if not TELEGRAM_TOKEN or not chat_id:
        print("[Telegram] Missing token or chat_id for photo")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    try:
        with open(image_path, "rb") as image_file:
            files = {"photo": image_file}
            data = {"chat_id": chat_id, "caption": caption}
            res = requests.post(url, files=files, data=data)
            return res.status_code == 200
    except Exception as e:
        print("[Telegram Photo Error]", e)
        return False
