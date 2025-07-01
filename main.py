import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# راه‌اندازی یک سرور ساده HTTP برای اینکه Render پورت 10000 رو تشخیص بده
def run_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running...")

    server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
    server.serve_forever()

# اجرا در یک ترد جداگانه
threading.Thread(target=run_http_server, daemon=True).start()

# ---------------- ربات ---------------- #

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات Renderی شما هستم.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, echo))
    await app.run_polling()

# اجرای ربات به‌صورت async
if __name__ == "__main__":
    asyncio.run(main())
