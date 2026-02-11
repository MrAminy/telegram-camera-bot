import os
import secrets
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_URL = os.getenv("SITE_URL")   # مثال: http://127.0.0.1:5000
CHANNEL_USERNAME = "@Mr_Aminy_Channel"

TEXT = {
    "fa": {
        "welcome": "👋 خوش آمدید\n\nلطفاً زبان خود را انتخاب کنید:",
        "join": "🔒 برای ادامه باید عضو کانال باشید:",
        "check": "✅ عضو شدم",
        "join_btn": "📢 عضویت در کانال",
        "not_member": "❌ هنوز عضو کانال نیستید.",
        "verified": "✅ عضویت تایید شد!\n\n🔗 لینک اختصاصی شما:",
        "open": "🌐 رفتن به وب‌سایت"
    },
    "en": {
        "welcome": "👋 Welcome\n\nPlease select your language:",
        "join": "🔒 To continue, join our channel:",
        "check": "✅ I Joined",
        "join_btn": "📢 Join Channel",
        "not_member": "❌ You are not a channel member yet.",
        "verified": "✅ Membership verified!\n\n🔗 Your private link:",
        "open": "🌐 Open Website"
    }
}

async def is_member(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🇦🇫 دری", callback_data="lang_fa"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]]
    )
    await update.message.reply_text(TEXT["fa"]["welcome"], reply_markup=keyboard)

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    t = TEXT[lang]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t["join_btn"], url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton(t["check"], callback_data="check_join")]
    ])

    await query.edit_message_text(f"{t['join']}\n{CHANNEL_USERNAME}", reply_markup=keyboard)

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

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(t["open"], url=link)]])
    await query.edit_message_text(f"{t['verified']}\n\n{link}", reply_markup=keyboard)

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(set_lang, pattern="^lang_"))
application.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))

def start_bot():
    print("🤖 Bot started")
    application.run_polling()