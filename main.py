import threading
import app
import bot
import os

def run_flask():
    app.app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def run_bot():
    bot.app.run_polling()

threading.Thread(target=run_flask).start()
threading.Thread(target=run_bot).start()
