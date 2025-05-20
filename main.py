# main.py
import pyttsx3
import schedule
import threading
import requests
import time
from openai import OpenAI
from datetime import datetime

# CONFIG
openai_api_key = "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"
TELEGRAM_BOT_TOKEN = "7566385345:AAEoHcXrvflQuBWjwr5XHy78C5kTiCNcbj8"
TELEGRAM_CHAT_ID = "7525736514"

client = OpenAI(api_key=openai_api_key)
engine = pyttsx3.init()

# Kirim pesan ke Telegram
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        res = requests.post(url, data=payload)
        return res.status_code == 200
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

# Kirim suara ke Telegram
def send_voice(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
    try:
        with open(file_path, 'rb') as voice:
            files = {'voice': voice}
            data = {'chat_id': TELEGRAM_CHAT_ID}
            res = requests.post(url, files=files, data=data)
            return res.status_code == 200
    except Exception as e:
        print(f"Voice Send Error: {e}")
        return False

# Minta berita dari ChatGPT
def ask_gpt(topic):
    prompt = f"Berikan saya 3 berita {topic} terbaru hari ini, ringkas masing-masing dalam 2 kalimat."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Gagal ambil berita: {e}"

# Jadwal rutin berita

def send_news():
    topics = [
        ("militer dunia dan Indonesia", "🪖 Militer"),
        ("ekonomi Indonesia dan dunia", "💰 Ekonomi"),
        ("internasional yang sedang viral", "🌍 Global")
    ]
    for topic, label in topics:
        berita = ask_gpt(topic)
        message = f"{label} News:\n\n{berita}"
        send_to_telegram(message)
        time.sleep(2)

# Jadwal kirim pengingat suara
def schedule_jobs():
    schedule.every().day.at("07:00").do(send_news)
    schedule.every().day.at("18:00").do(send_news)
    schedule.every().day.at("13:00").do(lambda: send_voice("reminder_13.wav"))
    schedule.every().day.at("21:00").do(lambda: send_voice("reminder_21.wav"))
    while True:
        schedule.run_pending()
        time.sleep(30)

# Jalankan
if __name__ == '__main__':
    threading.Thread(target=schedule_jobs, daemon=True).start()
    print("Brian is running in the cloud...")
    while True:
        time.sleep(60)
