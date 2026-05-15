from telegram import Update
from telegram.ext import ContextTypes


WELCOME_TEXT = (
    "👋 Assalomu alaykum!\n\n"
    "🤖 Men PDF bilan ishlovchi botman. Quyidagilarni qila olaman:\n\n"
    "📸 *Rasm → PDF*\n"
    "Rasmlarni yuboring va /done bosing.\n\n"
    "📄 *PDF amallari*\n"
    "PDF yuboring, tugmadan tanlang:\n"
    "  • Rasmga aylantirish\n"
    "  • Sahifalarga bo'lish\n"
    "  • Birlashtirish (merge)\n\n"
    "ℹ️ Batafsil: /help"
)


HELP_TEXT = (
    "📖 *Yordam*\n\n"
    "📸 *Rasmdan PDF yasash:*\n"
    "1. Bir yoki bir nechta rasm yuboring\n"
    "2. /done — barchasini bitta PDF qiladi\n\n"
    "📄 *PDF bilan ishlash:*\n"
    "PDF fayl yuborganingizda menyu chiqadi:\n"
    "  • 📷 *Rasmga aylantirish* — har sahifani rasm qiladi\n"
    "  • ✂️ *Sahifalarga bo'lish* — alohida fayllarga ajratadi\n"
    "  • ➕ *Birlashtirish* — keyingi PDF'lar bilan qo'shadi\n\n"
    "🎯 *Komandalar:*\n"
    "/start — botni qayta ishga tushirish\n"
    "/done — joriy amalni yakunlash\n"
    "/cancel — bekor qilish va tozalash\n"
    "/reset — /cancel ning sinonimi\n"
    "/help — shu yordam matni\n\n"
    "⚠️ *Cheklovlar:*\n"
    "• Maksimal fayl o'lchami: 20MB\n"
    "• Maksimal 50 ta rasm yoki 10 ta PDF"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(WELCOME_TEXT, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    had_state = bool(
        context.user_data.get("images")
        or context.user_data.get("merge_pdfs")
        or context.user_data.get("pending_pdf")
        or context.user_data.get("mode")
    )
    context.user_data.clear()
    if had_state:
        await update.message.reply_text("🗑 Tozalandi. Yangidan boshlashingiz mumkin.")
    else:
        await update.message.reply_text("ℹ️ Hech narsa yo'q edi. Rasm yoki PDF yuboring.")
