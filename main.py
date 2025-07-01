import os
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# اجرای HTTP server برای باز نگه‌داشتن پورت
def run_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running...")
    server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

# توکن ربات از متغیر محیطی
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# لیست عکس‌ها (میتونی با URL عکس‌های دلخواه جایگزین کنی)
PHOTO_URLS = [
    "https://picsum.photos/seed/a/400",
    "https://picsum.photos/seed/b/400",
    "https://picsum.photos/seed/c/400",
    "https://picsum.photos/seed/d/400",
    "https://picsum.photos/seed/e/400"
]

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📷 دریافت عکس", callback_data="get_image")],
        [InlineKeyboardButton("📞 تماس با ما", url="https://t.me/YOUR_USERNAME")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# مدیریت دکمه‌ها
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_image":
        photo_url = random.choice(PHOTO_URLS)
        await query.message.reply_photo(photo=photo_url, caption="✅ عکس جدید برای شما")

# تکرار پیام کاربر
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# پیکربندی ربات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# اجرای ربات
app.run_polling(close_loop=False, drop_pending_updates=True)
