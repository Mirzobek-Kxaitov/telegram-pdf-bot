import logging
from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services import pdf_tools
from services.i18n import t

from . import get_lang

logger = logging.getLogger(__name__)


def _split_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_split_each", lang), callback_data="split_each")],
        [InlineKeyboardButton(t("btn_split_range", lang), callback_data="split_range")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="split_back")],
    ])


async def show_options(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    pages = context.user_data.get("pending_pdf_pages", 0)
    await query.edit_message_text(
        t("split_question", lang, pages=pages),
        reply_markup=_split_menu_keyboard(lang),
    )


async def do_each_page(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text(t("pdf_not_found", lang))
        return

    pages = context.user_data.get("pending_pdf_pages", 0)
    await query.edit_message_text(t("splitting_pages", lang, count=pages))

    try:
        parts = pdf_tools.split_pdf_each_page(pdf_bytes)
    except Exception:
        logger.exception("PDF har sahifaga bo'lishda xato")
        await query.edit_message_text(t("split_error", lang))
        return

    chat_id = query.message.chat_id
    try:
        for i, part in enumerate(parts, 1):
            await context.bot.send_document(
                chat_id=chat_id,
                document=BytesIO(part),
                filename=f"page_{i:03d}.pdf",
            )
        await context.bot.send_message(
            chat_id=chat_id,
            text=t("split_each_done", lang, count=len(parts)),
        )
    except Exception:
        logger.exception("Sahifalarni yuborishda xato")
        await context.bot.send_message(chat_id=chat_id, text=t("send_error", lang))
    finally:
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None


async def prompt_range(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    pages = context.user_data.get("pending_pdf_pages", 0)
    context.user_data["mode"] = "awaiting_split_range"
    await query.edit_message_text(
        t("range_prompt", lang, pages=pages),
        parse_mode="Markdown",
    )


async def handle_range_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    pdf_bytes = context.user_data.get("pending_pdf")
    pages = context.user_data.get("pending_pdf_pages", 0)
    range_str = update.message.text or ""

    if not pdf_bytes:
        await update.message.reply_text(t("pdf_not_found", lang))
        context.user_data["mode"] = None
        return

    try:
        groups = pdf_tools.parse_page_ranges(range_str, pages)
    except ValueError as e:
        await update.message.reply_text(t("range_error", lang, error=str(e)))
        return

    notice = await update.message.reply_text(
        t("splitting_range", lang, count=len(groups))
    )

    try:
        parts = pdf_tools.split_pdf_by_ranges(pdf_bytes, groups)
    except Exception:
        logger.exception("PDF diapazon bo'yicha bo'lishda xato")
        await update.message.reply_text(t("split_range_processing_error", lang))
        return

    chat_id = update.effective_chat.id
    try:
        for indices, part in zip(groups, parts):
            label = _format_range_label(indices)
            await context.bot.send_document(
                chat_id=chat_id,
                document=BytesIO(part),
                filename=f"split_{label}.pdf",
            )
        await context.bot.send_message(
            chat_id=chat_id,
            text=t("split_range_done", lang, count=len(parts)),
        )
    except Exception:
        logger.exception("Bo'laklarni yuborishda xato")
        await update.message.reply_text(t("split_range_send_error", lang))
    finally:
        try:
            await notice.delete()
        except Exception:
            pass
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None


def _format_range_label(indices: list[int]) -> str:
    if len(indices) == 1:
        return f"p{indices[0] + 1}"
    return f"p{indices[0] + 1}-{indices[-1] + 1}"
