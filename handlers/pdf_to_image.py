import logging
from io import BytesIO

from telegram import InputMediaPhoto
from telegram.ext import ContextTypes

from config import PAGES_AS_IMAGES_LIMIT
from services import pdf_tools
from services.i18n import t

from . import get_lang

logger = logging.getLogger(__name__)

MEDIA_GROUP_SIZE = 10


async def convert(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text(t("pdf_not_found", lang))
        return

    page_count = context.user_data.get("pending_pdf_pages", 0)
    await query.edit_message_text(t("converting_pages", lang, pages=page_count))

    try:
        images = pdf_tools.pdf_to_images(pdf_bytes)
    except Exception:
        logger.exception("PDF rasmga aylantirishda xato")
        await query.edit_message_text(t("pdf2img_error", lang))
        return

    chat_id = query.message.chat_id

    try:
        if len(images) <= PAGES_AS_IMAGES_LIMIT:
            for i in range(0, len(images), MEDIA_GROUP_SIZE):
                batch = images[i:i + MEDIA_GROUP_SIZE]
                media = [InputMediaPhoto(BytesIO(b)) for b in batch]
                await context.bot.send_media_group(chat_id=chat_id, media=media)
            await context.bot.send_message(
                chat_id=chat_id,
                text=t("images_sent", lang, count=len(images)),
            )
        else:
            zip_bytes = pdf_tools.images_to_zip(images)
            await context.bot.send_document(
                chat_id=chat_id,
                document=BytesIO(zip_bytes),
                filename="pages.zip",
                caption=t("images_as_zip", lang, count=len(images)),
            )
    except Exception:
        logger.exception("Rasmlarni yuborishda xato")
        await context.bot.send_message(chat_id=chat_id, text=t("send_error", lang))
    finally:
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None
