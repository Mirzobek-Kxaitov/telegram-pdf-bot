import os
import logging
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)

# Logging sozlamasi - botda nima bo'layotganini ko'rish uchun
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram token - environment variable'dan olamiz
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi /start bosganda"""
    context.user_data["images"] = []
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "📸 Menga bir yoki bir nechta rasm yuboring.\n"
        "✅ Tugatgach /done deb yozing — men ularni bitta PDF qilib beraman.\n"
        "🗑 Boshidan boshlash uchun /reset yozing."
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi /reset bosganda - rasmlarni tozalash"""
    context.user_data["images"] = []
    await update.message.reply_text("🗑 Rasmlar tozalandi. Yangi rasm yuborishingiz mumkin.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi oddiy rasm yuborganda (siqilgan sifat)"""
    try:
        if "images" not in context.user_data:
            context.user_data["images"] = []

        # Eng yuqori sifatli versiyasini olamiz
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        # Rasmni xotiraga yuklash
        buf = BytesIO()
        await file.download_to_memory(buf)
        buf.seek(0)

        image = Image.open(buf).convert("RGB")
        context.user_data["images"].append(image)

        count = len(context.user_data["images"])
        await update.message.reply_text(
            f"✅ Rasm qabul qilindi ({count} ta)\n"
            f"Yana yuboring yoki /done yozing."
        )
    except Exception as e:
        logger.error(f"Rasm xatosi: {e}")
        await update.message.reply_text(f"❌ Xato: {e}")


async def handle_image_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi rasmni fayl sifatida yuborganda (asl sifat)"""
    try:
        document = update.message.document
        if not document.mime_type or not document.mime_type.startswith("image/"):
            await update.message.reply_text(
                "⚠️ Iltimos, faqat rasm yuboring (jpg, png, va h.k.)"
            )
            return

        if "images" not in context.user_data:
            context.user_data["images"] = []

        file = await context.bot.get_file(document.file_id)
        buf = BytesIO()
        await file.download_to_memory(buf)
        buf.seek(0)

        image = Image.open(buf).convert("RGB")
        context.user_data["images"].append(image)

        count = len(context.user_data["images"])
        await update.message.reply_text(
            f"✅ Rasm qabul qilindi ({count} ta)\n"
            f"Yana yuboring yoki /done yozing."
        )
    except Exception as e:
        logger.error(f"Hujjat xatosi: {e}")
        await update.message.reply_text(f"❌ Xato: {e}")


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi /done bosganda - hamma rasmlarni PDF qilish"""
    images = context.user_data.get("images", [])

    if not images:
        await update.message.reply_text(
            "⚠️ Hech qanday rasm yuborilmagan.\n"
            "Avval rasm yuboring, keyin /done bosing."
        )
        return

    try:
        await update.message.reply_text(
            f"🔄 {len(images)} ta rasm PDF'ga aylantirilmoqda..."
        )

        # PDF yaratish xotirada
        pdf_buffer = BytesIO()
        first_image = images[0]
        other_images = images[1:] if len(images) > 1 else []

        first_image.save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=other_images
        )
        pdf_buffer.seek(0)

        # PDF'ni foydalanuvchiga yuborish
        await update.message.reply_document(
            document=pdf_buffer,
            filename="converted.pdf",
            caption=f"✅ Tayyor! {len(images)} ta rasm bitta PDF qilindi."
        )

        # Foydalanuvchi ma'lumotlarini tozalash
        context.user_data["images"] = []

    except Exception as e:
        logger.error(f"PDF yasashda xato: {e}")
        await update.message.reply_text(f"❌ PDF yasashda xato: {e}")


def main():
    """Botni ishga tushirish"""
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN o'rnatilmagan!")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handler'larni qo'shamiz
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_image_document))

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()