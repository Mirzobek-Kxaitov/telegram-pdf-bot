import logging
from io import BytesIO

from telegram.ext import ContextTypes

from services import pdf_tools
from services.i18n import t

from . import get_lang, send_done_footer

logger = logging.getLogger(__name__)


def _human_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / 1024 / 1024:.2f} MB"


async def compress(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text(t("pdf_not_found", lang))
        return

    pages = context.user_data.get("pending_pdf_pages", 0)
    original_size = len(pdf_bytes)
    await query.edit_message_text(t("compressing", lang, pages=pages))

    try:
        compressed = pdf_tools.compress_pdf(pdf_bytes)
    except Exception:
        logger.exception("PDF siqishda xato")
        await query.edit_message_text(t("compress_error", lang))
        return

    new_size = len(compressed)
    chat_id = query.message.chat_id

    if new_size >= original_size:
        await context.bot.send_message(chat_id=chat_id, text=t("already_compressed", lang))
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None
        await send_done_footer(query.message.chat, lang)
        return

    saved_percent = round((1 - new_size / original_size) * 100)
    caption = t(
        "compress_done",
        lang,
        orig=_human_size(original_size),
        new=_human_size(new_size),
        percent=saved_percent,
    )

    try:
        await context.bot.send_document(
            chat_id=chat_id,
            document=BytesIO(compressed),
            filename="compressed.pdf",
            caption=caption,
        )
    except Exception:
        logger.exception("Siqilgan PDF yuborishda xato")
        await context.bot.send_message(chat_id=chat_id, text=t("send_error", lang))
    finally:
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None
        await send_done_footer(query.message.chat, lang)
