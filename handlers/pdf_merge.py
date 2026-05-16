import logging
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from config import (
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    MAX_PDFS_IN_MERGE,
    MAX_TOTAL_USER_BYTES,
    MAX_TOTAL_USER_MB,
)
from services import pdf_tools
from services.i18n import t

from . import get_lang, send_done_footer, total_user_bytes

logger = logging.getLogger(__name__)


async def start_merge(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text(t("pdf_not_found", lang))
        return

    merge_list = context.user_data.setdefault("merge_pdfs", [])
    merge_list.append(pdf_bytes)
    context.user_data["mode"] = "merging"
    context.user_data.pop("pending_pdf", None)
    context.user_data.pop("pending_pdf_pages", None)

    await query.edit_message_text(t("merge_started", lang, count=len(merge_list)))


async def add_pdf_to_merge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    document = update.message.document

    if document.file_size and document.file_size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(t("merge_pdf_too_large", lang, mb=MAX_FILE_SIZE_MB))
        return

    merge_list = context.user_data.setdefault("merge_pdfs", [])
    if len(merge_list) >= MAX_PDFS_IN_MERGE:
        await update.message.reply_text(t("max_pdfs_reached", lang, max=MAX_PDFS_IN_MERGE))
        return

    try:
        file = await context.bot.get_file(document.file_id)
        buf = BytesIO()
        await file.download_to_memory(buf)
        pdf_bytes = buf.getvalue()
    except Exception:
        logger.exception("Merge uchun PDF yuklab olishda xato")
        await update.message.reply_text(t("merge_download_error", lang))
        return

    if total_user_bytes(context.user_data) + len(pdf_bytes) > MAX_TOTAL_USER_BYTES:
        await update.message.reply_text(t("merge_total_exceeded", lang, mb=MAX_TOTAL_USER_MB))
        return

    try:
        pdf_tools.get_pdf_page_count(pdf_bytes)
    except Exception:
        logger.exception("Merge uchun PDF o'qishda xato")
        await update.message.reply_text(t("broken_pdf", lang))
        return

    merge_list.append(pdf_bytes)
    await update.message.reply_text(t("pdf_added_to_merge", lang, count=len(merge_list)))


async def do_merge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    merge_list = context.user_data.get("merge_pdfs", [])
    if len(merge_list) < 2:
        await update.message.reply_text(t("merge_need_two", lang, count=len(merge_list)))
        return

    notice = await update.message.reply_text(t("merging", lang, count=len(merge_list)))

    try:
        merged = pdf_tools.merge_pdfs(merge_list)
    except Exception:
        logger.exception("Merge xatosi")
        await update.message.reply_text(t("merge_error", lang))
        return

    try:
        await update.message.reply_document(
            document=BytesIO(merged),
            filename="merged.pdf",
            caption=t("merge_done", lang, count=len(merge_list)),
        )
    except Exception:
        logger.exception("Merge natijasini yuborishda xato")
        await update.message.reply_text(t("merge_send_error", lang))
    finally:
        try:
            await notice.delete()
        except Exception:
            pass
        context.user_data["merge_pdfs"] = []
        context.user_data["mode"] = None
        await send_done_footer(update.effective_chat, lang)
