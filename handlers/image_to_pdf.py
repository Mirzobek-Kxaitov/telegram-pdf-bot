import logging
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from telegram import Update
from telegram.ext import ContextTypes

from config import (
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    MAX_IMAGES_PER_USER,
    MAX_TOTAL_USER_BYTES,
    MAX_TOTAL_USER_MB,
)

from . import total_user_bytes

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
    data = buf.getvalue()

    if total_user_bytes(context.user_data) + len(data) > MAX_TOTAL_USER_BYTES:
        await update.message.reply_text(
            f"⚠️ Jami {MAX_TOTAL_USER_MB}MB limit oshib ketadi. "
            f"/done bosing yoki /cancel bilan bekor qiling."
        )
        return

    try:
        Image.open(BytesIO(data)).verify()
    except (UnidentifiedImageError, Exception):
        await update.message.reply_text("❌ Bu rasm formati qo'llab-quvvatlanmaydi.")
        return

    images.append(data)

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


def _open_rgb(image_bytes: bytes) -> Image.Image:
    img = Image.open(BytesIO(image_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


async def images_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Called by /done when user is in image-collection mode."""
    image_bytes_list = context.user_data.get("images", [])
    if not image_bytes_list:
        await update.message.reply_text(
            "⚠️ Hech qanday rasm yuborilmagan.\n"
            "Avval rasm yuboring, keyin /done bosing."
        )
        return

    notice = await update.message.reply_text(
        f"🔄 {len(image_bytes_list)} ta rasm PDF'ga aylantirilmoqda..."
    )

    pdf_buffer = BytesIO()
    pil_images: list[Image.Image] = []
    try:
        pil_images = [_open_rgb(b) for b in image_bytes_list]
        first, *rest = pil_images
        first.save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=rest,
        )
        pdf_buffer.seek(0)

        await update.message.reply_document(
            document=pdf_buffer,
            filename="converted.pdf",
            caption=f"✅ Tayyor! {len(image_bytes_list)} ta rasm bitta PDF qilindi.",
        )
    except Exception:
        logger.exception("PDF yasashda xato")
        await update.message.reply_text(
            "❌ PDF yasashda xato yuz berdi. Iltimos, qayta urinib ko'ring."
        )
    finally:
        for img in pil_images:
            try:
                img.close()
            except Exception:
                pass
        try:
            await notice.delete()
        except Exception:
            pass
        context.user_data["images"] = []
