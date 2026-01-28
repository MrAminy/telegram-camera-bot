from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler,
    CallbackQueryHandler, ContextTypes
)
import os, secrets, sys

BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_URL = os.getenv("SITE_URL") or "http://127.0.0.1:5000"
CHANNEL_USERNAME = "@hack22_2"

if not BOT_TOKEN:
    print("❌ BOT_TOKEN ست نشده")
    sys.exit(1)

TEXT = {
    "fa": {
        "welcome": "👋 خوش آمدید\n\nزبان را انتخاب کنید:",
        "join": "🔒 برای ادامه عضو کانال شوید:",
        "check": "✅ عضو شدم",
        "join_btn": "📢 عضویت در کانال",
        "not_member": "❌ هنوز عضو کانال نیستید.",
        "verified": "✅ عضویت تایید شد!\n\nبرای ادامه روی دکمه زیر بزنید 👇",
        "open": "🌐 باز کردن سایت"
    },
    "en": {
        "welcome": "👋 Welcome\n\nSelect language:",
        "join": "🔒 To continue, join the channel:",
        "check": "✅ I Joined",
        "join_btn": "📢 Join Channel",
        "not_member": "❌ You are not a member yet.",
        "verified": "✅ Membership verified!\n\nClick below 👇",
        "open": "🌐 Open Website"
    }
}

async def is_member(bot, user_id):
    try:
        m = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇦🇫 دری", callback_data="lang_fa"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ])
    await update.message.reply_text(TEXT["fa"]["welcome"], reply_markup=kb)

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data.split("_")[1]
    context.user_data["lang"] = lang
    t = TEXT[lang]

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t["join_btn"], url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton(t["check"], callback_data="check_join")]
    ])
    await q.edit_message_text(f"{t['join']}\n{CHANNEL_USERNAME}", reply_markup=kb)

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = context.user_data.get("lang", "fa")
    t = TEXT[lang]

    if not await is_member(context.bot, q.from_user.id):
        await q.answer(t["not_member"], show_alert=True)
        return

    token = secrets.token_urlsafe(12)
    link = f"{SITE_URL}/?token={token}"

    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t["open"], url=link)]])
    await q.edit_message_text(t["verified"], reply_markup=kb)

def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_lang, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))
    print("🤖 Bot started")
    app.run_polling()
