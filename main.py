import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# اجرای HTTP server برای پورت ساختگی (ترفند Render)
def run_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running...")

    server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

# ---- ربات تلگرام ----

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات Renderی شما هستم.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# اجرای مستقیم بدون استفاده از asyncio.run()
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, echo))

# این نسخه اجرا می‌شه حتی اگر event loop قبلاً اجرا شده باشه
app.run_polling(close_loop=False)
