import threading
import time
import app
import bot

def run_flask():
    app.app.run(host="0.0.0.0", port=5000, debug=False)

def run_bot():
    bot.start_bot()

t1 = threading.Thread(target=run_flask, daemon=True)
t2 = threading.Thread(target=run_bot, daemon=True)

t1.start()
t2.start()

print("🚀 Flask + Telegram Bot are running")

while True:
    time.sleep(10)
