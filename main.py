import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# اجرای HTTP Server برای باز نگه‌داشتن پورت (ترفند Render)
def run_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running...")

    server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

# --- ربات تلگرام ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# دستور start همراه با دکمه‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📷 دریافت عکس", callback_data="get_image")],
        [InlineKeyboardButton("📞 تماس با ما", url="https://t.me/YOUR_USERNAME")],  # ← یوزرنیم خودت رو جایگزین کن
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# پاسخ به کلیک دکمه‌ها
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_image":
        await query.message.reply_photo(
            photo="https://picsum.photos/400",  # می‌تونی عکس دلخواه خودت رو بذاری
            caption="اینم عکس شما 😊"
        )

# اکو برای تست پیام‌های متنی
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# ایجاد اپلیکیشن و ثبت هندلرها
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# اجرای ربات
app.run_polling(close_loop=False)
