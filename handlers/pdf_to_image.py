import logging
from io import BytesIO

from telegram import InputMediaPhoto
from telegram.ext import ContextTypes

from config import PAGES_AS_IMAGES_LIMIT
from services import pdf_tools

logger = logging.getLogger(__name__)

MEDIA_GROUP_SIZE = 10


async def convert(query, context: ContextTypes.DEFAULT_TYPE):
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text(
            "⚠️ PDF topilmadi. Iltimos, PDF'ni qaytadan yuboring."
        )
        return

    page_count = context.user_data.get("pending_pdf_pages", 0)
    await query.edit_message_text(
        f"🔄 {page_count} ta sahifa rasmga aylantirilmoqda..."
    )

    try:
        images = pdf_tools.pdf_to_images(pdf_bytes)
    except Exception:
        logger.exception("PDF rasmga aylantirishda xato")
        await query.edit_message_text(
            "❌ PDF'ni rasmga aylantirib bo'lmadi."
        )
        return

    chat_id = query.message.chat_id

    try:
        if len(images) <= PAGES_AS_IMAGES_LIMIT:
            for i in range(0, len(images), MEDIA_GROUP_SIZE):
                batch = images[i:i + MEDIA_GROUP_SIZE]
                media = [InputMediaPhoto(BytesIO(b)) for b in batch]
                await context.bot.send_media_group(chat_id=chat_id, media=media)
            caption = f"✅ {len(images)} ta sahifa yuborildi."
        else:
            zip_bytes = pdf_tools.images_to_zip(images)
            await context.bot.send_document(
                chat_id=chat_id,
                document=BytesIO(zip_bytes),
                filename="pages.zip",
                caption=f"✅ {len(images)} ta sahifa rasm sifatida ZIP arxivda."
            )
            caption = None

        if caption:
            await context.bot.send_message(chat_id=chat_id, text=caption)
    except Exception:
        logger.exception("Rasmlarni yuborishda xato")
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Rasmlarni yuborishda xato yuz berdi."
        )
    finally:
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None
