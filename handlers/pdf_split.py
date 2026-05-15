import logging
from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services import pdf_tools

logger = logging.getLogger(__name__)


def _split_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 Har sahifa alohida", callback_data="split_each")],
        [InlineKeyboardButton("🎯 Diapazon kiritaman", callback_data="split_range")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="split_back")],
    ])


async def show_options(query, context: ContextTypes.DEFAULT_TYPE):
    pages = context.user_data.get("pending_pdf_pages", 0)
    await query.edit_message_text(
        f"✂️ PDF ({pages} sahifa) qanday bo'linsin?",
        reply_markup=_split_menu_keyboard(),
    )


async def do_each_page(query, context: ContextTypes.DEFAULT_TYPE):
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text("⚠️ PDF topilmadi. Qaytadan yuboring.")
        return

    pages = context.user_data.get("pending_pdf_pages", 0)
    await query.edit_message_text(f"🔄 {pages} ta sahifa ajratilmoqda...")

    try:
        parts = pdf_tools.split_pdf_each_page(pdf_bytes)
    except Exception:
        logger.exception("PDF har sahifaga bo'lishda xato")
        await query.edit_message_text("❌ PDF'ni bo'lib bo'lmadi.")
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
            text=f"✅ {len(parts)} ta alohida PDF yuborildi."
        )
    except Exception:
        logger.exception("Sahifalarni yuborishda xato")
        await context.bot.send_message(chat_id=chat_id, text="❌ Yuborishda xato.")
    finally:
        context.user_data.pop("pending_pdf", None)
        context.user_data.pop("pending_pdf_pages", None)
        context.user_data["mode"] = None


async def prompt_range(query, context: ContextTypes.DEFAULT_TYPE):
    pages = context.user_data.get("pending_pdf_pages", 0)
    context.user_data["mode"] = "awaiting_split_range"
    await query.edit_message_text(
        f"🎯 Diapazonni kiriting (PDF da {pages} ta sahifa):\n\n"
        f"Misol:\n"
        f"• `1-3` — 1-dan 3-gacha bitta PDF\n"
        f"• `1-3, 5-7` — ikkita alohida PDF\n"
        f"• `1, 3, 5` — uchta alohida sahifa\n\n"
        f"Bekor qilish uchun /cancel",
        parse_mode="Markdown",
    )


async def handle_range_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_bytes = context.user_data.get("pending_pdf")
    pages = context.user_data.get("pending_pdf_pages", 0)
    range_str = update.message.text or ""

    if not pdf_bytes:
        await update.message.reply_text("⚠️ PDF topilmadi. Qaytadan yuboring.")
        context.user_data["mode"] = None
        return

    try:
        groups = pdf_tools.parse_page_ranges(range_str, pages)
    except ValueError as e:
        await update.message.reply_text(
            f"❌ {e}\n\nQaytadan urinib ko'ring yoki /cancel bosing."
        )
        return

    notice = await update.message.reply_text(
        f"🔄 {len(groups)} ta qism ajratilmoqda..."
    )

    try:
        parts = pdf_tools.split_pdf_by_ranges(pdf_bytes, groups)
    except Exception:
        logger.exception("PDF diapazon bo'yicha bo'lishda xato")
        await update.message.reply_text("❌ Bo'lishda xato yuz berdi.")
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
            text=f"✅ {len(parts)} ta PDF yuborildi."
        )
    except Exception:
        logger.exception("Bo'laklarni yuborishda xato")
        await update.message.reply_text("❌ Yuborishda xato.")
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
