import schedule
import time
from utils.settings import load_settings
from utils.ai import generate_signal
from utils.telegram import send_message

def schedule_signals():
    settings = load_settings()
    for t in settings["signal_schedule"]:
        schedule.every().day.at(t).do(send_scheduled_signal)

def send_scheduled_signal():
    signal, conf, price = generate_signal("BTC/USD")
    send_message(f"🕒 Scheduled Signal: {signal} at ${price:.2f} (Conf: {conf}%)")

if __name__ == "__main__":
    schedule_signals()
    while True:
        schedule.run_pending()
        time.sleep(1)
