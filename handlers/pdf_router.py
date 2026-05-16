import logging
from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import (
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    MAX_TOTAL_USER_BYTES,
    MAX_TOTAL_USER_MB,
)
from services import pdf_tools
from services.i18n import t

from . import (
    get_lang,
    image_to_pdf,
    language_keyboard,
    pdf_compress,
    pdf_merge,
    pdf_password,
    pdf_split,
    pdf_to_image,
    total_user_bytes,
)

logger = logging.getLogger(__name__)


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_pdf2img", lang), callback_data="pdf2img")],
        [InlineKeyboardButton(t("btn_split", lang), callback_data="split_menu")],
        [InlineKeyboardButton(t("btn_merge", lang), callback_data="merge_start")],
        [InlineKeyboardButton(t("btn_compress", lang), callback_data="compress")],
        [InlineKeyboardButton(t("btn_password_set", lang), callback_data="password_set")],
        [InlineKeyboardButton(t("btn_cancel", lang), callback_data="cancel")],
    ])


def encrypted_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_password_remove", lang), callback_data="password_remove")],
        [InlineKeyboardButton(t("btn_cancel", lang), callback_data="cancel")],
    ])


async def handle_pdf_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type != "application/pdf":
        return

    lang = get_lang(context, update.effective_user)

    if document.file_size and document.file_size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(t("pdf_too_large", lang, mb=MAX_FILE_SIZE_MB))
        return

    if context.user_data.get("mode") == "merging":
        await pdf_merge.add_pdf_to_merge(update, context)
        return

    try:
        file = await context.bot.get_file(document.file_id)
        buf = BytesIO()
        await file.download_to_memory(buf)
        pdf_bytes = buf.getvalue()
    except Exception:
        logger.exception("PDF yuklab olishda xato")
        await update.message.reply_text(t("pdf_download_error", lang))
        return

    if total_user_bytes(context.user_data) + len(pdf_bytes) > MAX_TOTAL_USER_BYTES:
        await update.message.reply_text(t("total_size_exceeded", lang, mb=MAX_TOTAL_USER_MB))
        return

    try:
        encrypted = pdf_tools.is_pdf_encrypted(pdf_bytes)
    except Exception:
        logger.exception("PDF o'qishda xato")
        await update.message.reply_text(t("pdf_read_error", lang))
        return

    if encrypted:
        context.user_data["pending_pdf"] = pdf_bytes
        context.user_data["pending_pdf_pages"] = None
        context.user_data["pending_pdf_encrypted"] = True
        context.user_data["mode"] = "pdf_received"
        await update.message.reply_text(
            t("pdf_encrypted_received", lang),
            reply_markup=encrypted_menu_keyboard(lang),
        )
        return

    try:
        page_count = pdf_tools.get_pdf_page_count(pdf_bytes)
    except Exception:
        logger.exception("PDF sahifa sonini o'qishda xato")
        await update.message.reply_text(t("pdf_page_read_error", lang))
        return

    context.user_data["pending_pdf"] = pdf_bytes
    context.user_data["pending_pdf_pages"] = page_count
    context.user_data["pending_pdf_encrypted"] = False
    context.user_data["mode"] = "pdf_received"

    await update.message.reply_text(
        t("pdf_received", lang, pages=page_count),
        reply_markup=main_menu_keyboard(lang),
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    lang = get_lang(context, query.from_user)

    if action == "cancel":
        saved_lang = context.user_data.get("lang")
        context.user_data.clear()
        if saved_lang:
            context.user_data["lang"] = saved_lang
        await query.edit_message_text(t("cancelled", lang))
        return

    if action == "pdf2img":
        await pdf_to_image.convert(query, context)
    elif action == "split_menu":
        await pdf_split.show_options(query, context)
    elif action == "split_each":
        await pdf_split.do_each_page(query, context)
    elif action == "split_range":
        await pdf_split.prompt_range(query, context)
    elif action == "split_back":
        pages = context.user_data.get("pending_pdf_pages", "?")
        await query.edit_message_text(
            t("pdf_back_menu", lang, pages=pages),
            reply_markup=main_menu_keyboard(lang),
        )
    elif action == "merge_start":
        await pdf_merge.start_merge(query, context)
    elif action == "compress":
        await pdf_compress.compress(query, context)
    elif action == "password_set":
        await pdf_password.prompt_set_password(query, context)
    elif action == "password_remove":
        await pdf_password.prompt_remove_password(query, context)
    elif action == "show_help":
        await query.message.chat.send_message(t("help", lang), parse_mode="Markdown")
    elif action == "show_language":
        await query.message.chat.send_message(
            t("language_prompt", lang),
            reply_markup=language_keyboard(),
        )
    else:
        await query.edit_message_text(t("unknown_action", lang))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    if mode == "awaiting_split_range":
        await pdf_split.handle_range_text(update, context)
    elif mode in ("awaiting_password_set", "awaiting_password_remove"):
        await pdf_password.handle_password_text(update, context)
    elif mode == "awaiting_reorder":
        await image_to_pdf.handle_reorder_text(update, context)
