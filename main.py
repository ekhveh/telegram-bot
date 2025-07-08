import os
import random
import threading
import openai
# کلید API از محیط (در Render ذخیره کن)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

async def get_joke_from_chatgpt():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # یا gpt-4 اگه دسترسی داری
            messages=[
                {"role": "system", "content": "تو یه کمدین باحال هستی"},
                {"role": "user", "content": "یه جوک بامزه و خفن درباره رابطه دختر و پدر بگو"}
            ],
            max_tokens=100,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"خطا در دریافت جوک: {e}"

# اجرای HTTP server برای نگه‌داشتن پورت در Render
def run_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running...")
    server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_http_server, daemon=True).start()

# دریافت توکن از محیط
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# عکس‌ها به تفکیک دسته‌بندی
PHOTO_CATEGORIES = {
    "طبیعت": [
        "https://picsum.photos/seed/nature1/400",
        "https://picsum.photos/seed/nature2/400",
        "https://picsum.photos/seed/nature3/400"
    ],
    "فضا": [
        "https://picsum.photos/seed/space1/400",
        "https://picsum.photos/seed/space2/400",
        "https://picsum.photos/seed/space3/400"
    ],
    "حیوانات": [
        "https://picsum.photos/seed/animal1/400",
        "https://picsum.photos/seed/animal2/400",
        "https://picsum.photos/seed/animal3/400"
    ]
}

# لیست عمومی همه عکس‌ها برای ارسال ۳تایی
ALL_PHOTOS = sum(PHOTO_CATEGORIES.values(), [])

# کپشن‌های تصادفی
CAPTIONS = [
    "🌿 زیبایی طبیعت در قاب تصویر",
    "🚀 نگاهی به آسمان بی‌نهایت",
    "🐾 لحظه‌ای با دنیای حیوانات",
    "📷 لحظه‌ای برای تأمل",
    "✨ زیبایی در سادگی"
]

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📷 عکس طبیعت", callback_data="cat_طبیعت")],
        [InlineKeyboardButton("🚀 عکس فضا", callback_data="cat_فضا")],
        [InlineKeyboardButton("🐶 عکس حیوانات", callback_data="cat_حیوانات")],
        [InlineKeyboardButton("🖼 دریافت ۳ عکس تصادفی", callback_data="get_3_images")],
        [InlineKeyboardButton("📞 تماس با ما", url="https://t.me/YOUR_USERNAME")],
        [InlineKeyboardButton("🤣 گفتن جوک خفن", callback_data="get_joke")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# مدیریت کلیک دکمه‌ها
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("cat_"):
        category = query.data.replace("cat_", "")
        photo_url = random.choice(PHOTO_CATEGORIES[category])
        caption = random.choice(CAPTIONS)
        await query.message.reply_photo(photo=photo_url, caption=f"{caption}\n📁 دسته: {category}")

    elif query.data == "get_3_images":
        for i in range(3):
            photo_url = random.choice(ALL_PHOTOS)
            caption = random.choice(CAPTIONS)
            await query.message.reply_photo(photo=photo_url, caption=f"{caption} ({i+1}/3)")
    elif query.data == "get_joke":
       await query.message.reply_text("دارم دنبال یه جوک خفن می‌گردم... 😁")
       joke = await get_joke_from_chatgpt()
       await query.message.reply_text(joke)

# تکرار پیام کاربر (در صورت نیاز)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# پیکربندی و اجرای بات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling(close_loop=False, drop_pending_updates=True)
