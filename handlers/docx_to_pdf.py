import logging
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB
from services import docx_tools
from services.i18n import t

from . import get_lang, send_done_footer

logger = logging.getLogger(__name__)


async def handle_docx_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    lang = get_lang(context, update.effective_user)

    if document.file_size and document.file_size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(t("docx_too_large", lang, mb=MAX_FILE_SIZE_MB))
        return

    notice = await update.message.reply_text(t("docx_converting", lang))

    try:
        file = await context.bot.get_file(document.file_id)
        buf = BytesIO()
        await file.download_to_memory(buf)
        docx_bytes = buf.getvalue()
    except Exception:
        logger.exception("DOCX yuklab olishda xato")
        try:
            await notice.delete()
        except Exception:
            pass
        await update.message.reply_text(t("docx_download_error", lang))
        return

    try:
        pdf_bytes = docx_tools.docx_to_pdf(docx_bytes)
    except Exception:
        logger.exception("DOCX konvertatsiyada xato")
        try:
            await notice.delete()
        except Exception:
            pass
        await update.message.reply_text(t("docx_convert_error", lang))
        return

    try:
        original_name = document.file_name or "document.docx"
        pdf_name = original_name.rsplit(".", 1)[0] + ".pdf"
        await update.message.reply_document(
            document=BytesIO(pdf_bytes),
            filename=pdf_name,
            caption=t("docx_done", lang),
        )
    except Exception:
        logger.exception("DOCX→PDF yuborishda xato")
        await update.message.reply_text(t("send_error", lang))
    finally:
        try:
            await notice.delete()
        except Exception:
            pass
        await send_done_footer(update.effective_chat, lang)
