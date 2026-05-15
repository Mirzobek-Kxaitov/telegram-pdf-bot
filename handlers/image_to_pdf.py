import logging
from io import BytesIO

from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB, MAX_IMAGES_PER_USER

logger = logging.getLogger(__name__)


async def _store_image(update: Update, context: ContextTypes.DEFAULT_TYPE, file, size: int | None):
    if size and size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(
            f"❌ Rasm juda katta. Maksimal {MAX_FILE_SIZE_MB}MB."
        )
        return

    images = context.user_data.setdefault("images", [])
    if len(images) >= MAX_IMAGES_PER_USER:
        await update.message.reply_text(
            f"⚠️ Maksimal {MAX_IMAGES_PER_USER} ta rasm yuborildi. "
            f"/done bosing yoki /cancel bilan bekor qiling."
        )
        return

    buf = BytesIO()
    await file.download_to_memory(buf)
    buf.seek(0)
    image = Image.open(buf).convert("RGB")
    images.append(image)

    count = len(images)
    await update.message.reply_text(
        f"✅ Rasm qabul qilindi ({count} ta)\nYana yuboring yoki /done yozing."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        await _store_image(update, context, file, photo.file_size)
    except Exception:
        logger.exception("Rasm qabul qilishda xato")
        await update.message.reply_text("❌ Rasmni qabul qilib bo'lmadi.")


async def handle_image_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        document = update.message.document
        if not document.mime_type or not document.mime_type.startswith("image/"):
            await update.message.reply_text(
                "⚠️ Iltimos, faqat rasm yuboring (jpg, png, va h.k.)"
            )
            return
        file = await context.bot.get_file(document.file_id)
        await _store_image(update, context, file, document.file_size)
    except Exception:
        logger.exception("Hujjat qabul qilishda xato")
        await update.message.reply_text("❌ Faylni qabul qilib bo'lmadi.")


async def images_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Called by /done when user is in image-collection mode."""
    images = context.user_data.get("images", [])
    if not images:
        await update.message.reply_text(
            "⚠️ Hech qanday rasm yuborilmagan.\n"
            "Avval rasm yuboring, keyin /done bosing."
        )
        return

    notice = await update.message.reply_text(
        f"🔄 {len(images)} ta rasm PDF'ga aylantirilmoqda..."
    )

    try:
        pdf_buffer = BytesIO()
        first_image, *other_images = images
        first_image.save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=other_images,
        )
        pdf_buffer.seek(0)

        await update.message.reply_document(
            document=pdf_buffer,
            filename="converted.pdf",
            caption=f"✅ Tayyor! {len(images)} ta rasm bitta PDF qilindi.",
        )
    except Exception:
        logger.exception("PDF yasashda xato")
        await update.message.reply_text(
            "❌ PDF yasashda xato yuz berdi. Iltimos, qayta urinib ko'ring."
        )
    finally:
        try:
            await notice.delete()
        except Exception:
            pass
        context.user_data["images"] = []
