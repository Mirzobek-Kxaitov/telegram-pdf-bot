import logging
from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB
from services import pdf_tools

from . import pdf_merge, pdf_split, pdf_to_image

logger = logging.getLogger(__name__)


def _main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📷 Rasmga aylantirish", callback_data="pdf2img")],
        [InlineKeyboardButton("✂️ Sahifalarga bo'lish", callback_data="split_menu")],
        [InlineKeyboardButton("➕ Birlashtirish (merge)", callback_data="merge_start")],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")],
    ])


async def handle_pdf_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type != "application/pdf":
        return

    if document.file_size and document.file_size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(
            f"❌ PDF juda katta. Maksimal {MAX_FILE_SIZE_MB}MB."
        )
        return

    if context.user_data.get("mode") == "merging":
        await pdf_merge.add_pdf_to_merge(update, context)
        return

    try:
        file = await context.bot.get_file(document.file_id)
        buf = BytesIO()
        await file.download_to_memory(buf)
        pdf_bytes = buf.getvalue()
        page_count = pdf_tools.get_pdf_page_count(pdf_bytes)
    except Exception:
        logger.exception("PDF yuklab olishda xato")
        await update.message.reply_text(
            "❌ PDF faylni o'qib bo'lmadi. Fayl buzilgan bo'lishi mumkin."
        )
        return

    context.user_data["pending_pdf"] = pdf_bytes
    context.user_data["pending_pdf_pages"] = page_count
    context.user_data["mode"] = "pdf_received"

    await update.message.reply_text(
        f"📄 PDF qabul qilindi ({page_count} sahifa).\n\nNima qilamiz?",
        reply_markup=_main_menu_keyboard(),
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "cancel":
        context.user_data.clear()
        await query.edit_message_text("❌ Bekor qilindi.")
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
        await query.edit_message_text(
            f"📄 PDF ({context.user_data.get('pending_pdf_pages', '?')} sahifa). Nima qilamiz?",
            reply_markup=_main_menu_keyboard(),
        )
    elif action == "merge_start":
        await pdf_merge.start_merge(query, context)
    else:
        await query.edit_message_text("⚠️ Noma'lum amal.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generic text handler — only acts in awaiting_split_range mode."""
    if context.user_data.get("mode") == "awaiting_split_range":
        await pdf_split.handle_range_text(update, context)
