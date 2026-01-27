from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler,
    CallbackQueryHandler, ContextTypes
)
import secrets
import os

    BOT_TOKEN = os.getenv("8363284926:AAFwxSRfckAsXdF8gIqMx91cTA9xeNDO1CY")
CHANNEL_USERNAME = "@hack22_2"
SITE_URL = os.getenv("https://userverify.onrender.com")

# متن‌ها
TEXT = {
    "fa": {
        "welcome": "👋 خوش آمدید\n\nلطفاً زبان خود را انتخاب کنید:",
        "join": "🔒 برای ادامه باید عضو کانال باشید:",
        "check": "✅ عضو شدم",
        "join_btn": "📢 عضویت در کانال",
        "not_member": "❌ هنوز عضو کانال نیستید.",
        "verified": "✅ عضویت تایید شد!\n\nبرای ادامه روی دکمه زیر بزنید 👇",
        "open": "🌐 باز کردن سایت"
    },
    "en": {
        "welcome": "👋 Welcome\n\nPlease select your language:",
        "join": "🔒 To continue, join our channel:",
        "check": "✅ I Joined",
        "join_btn": "📢 Join Channel",
        "not_member": "❌ You are not a channel member yet.",
        "verified": "✅ Membership verified!\n\nClick below to continue 👇",
        "open": "🌐 Open Website"
    }
}

async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇦🇫 دری", callback_data="lang_fa"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ])
    await update.message.reply_text(TEXT["fa"]["welcome"], reply_markup=kb)

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    t = TEXT[lang]

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t["join_btn"], url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton(t["check"], callback_data="check_join")]
    ])

    await query.edit_message_text(
        f"{t['join']}\n{CHANNEL_USERNAME}",
        reply_markup=kb
    )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "fa")
    t = TEXT[lang]

    if not await is_member(context.bot, query.from_user.id):
        await query.edit_message_text(t["not_member"])
        return

    token = secrets.token_urlsafe(12)
    link = f"{SITE_URL}/?token={token}"

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t["open"], url=link)]
    ])

    await query.edit_message_text(
        t["verified"],
        reply_markup=kb
    )

# ⬇️ مهم: فقط اپلیکیشن را بساز، اجرا نکن
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(set_lang, pattern="lang_"))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
