import threading
import os
import app
import bot

def run_flask():
    app.app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

if __name__ == "__main__":
    # Flask در Thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Bot در main thread
    bot.start_bot()