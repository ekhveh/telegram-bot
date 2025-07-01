import os
import asyncio
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# برای فریب Render - باز کردن یک پورت بی‌استفاده
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.environ["BOT_TOKEN"]

# راه‌اندازی HTTP سرور ساده برای باز کردن پورت و جلوگیری از خطای Render
def run_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running...")

    server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
    server.serve_forever()

# اجرای HTTP سرور در ترد جدا
threading.Thread(target=run_http_server, daemon=True).start()

# ---- ربات تلگرام ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات Renderی شما هستم.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()
