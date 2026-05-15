import logging
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB, MAX_PDFS_IN_MERGE
from services import pdf_tools

logger = logging.getLogger(__name__)


async def start_merge(query, context: ContextTypes.DEFAULT_TYPE):
    pdf_bytes = context.user_data.get("pending_pdf")
    if not pdf_bytes:
        await query.edit_message_text("⚠️ PDF topilmadi. Qaytadan yuboring.")
        return

    merge_list = context.user_data.setdefault("merge_pdfs", [])
    merge_list.append(pdf_bytes)
    context.user_data["mode"] = "merging"
    context.user_data.pop("pending_pdf", None)
    context.user_data.pop("pending_pdf_pages", None)

    await query.edit_message_text(
        f"➕ Birlashtirish boshlandi. Hozir {len(merge_list)} ta PDF tayyor.\n\n"
        f"Yana PDF yuboring va keyin /done bosing.\n"
        f"Bekor qilish uchun /cancel."
    )


async def add_pdf_to_merge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Called when a PDF arrives while in merging mode."""
    document = update.message.document

    if document.file_size and document.file_size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(
            f"❌ PDF juda katta. Maksimal {MAX_FILE_SIZE_MB}MB."
        )
        return

    merge_list = context.user_data.setdefault("merge_pdfs", [])
    if len(merge_list) >= MAX_PDFS_IN_MERGE:
        await update.message.reply_text(
            f"⚠️ Maksimal {MAX_PDFS_IN_MERGE} ta PDF. /done bosing."
        )
        return

    try:
        file = await context.bot.get_file(document.file_id)
        buf = BytesIO()
        await file.download_to_memory(buf)
        pdf_bytes = buf.getvalue()
        pdf_tools.get_pdf_page_count(pdf_bytes)
    except Exception:
        logger.exception("Merge uchun PDF yuklab olishda xato")
        await update.message.reply_text("❌ PDF'ni qabul qilib bo'lmadi.")
        return

    merge_list.append(pdf_bytes)
    await update.message.reply_text(
        f"✅ Qo'shildi ({len(merge_list)} ta). Yana yuboring yoki /done bosing."
    )


async def do_merge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Called by /done when in merging mode."""
    merge_list = context.user_data.get("merge_pdfs", [])
    if len(merge_list) < 2:
        await update.message.reply_text(
            f"⚠️ Birlashtirish uchun kamida 2 ta PDF kerak. Hozir {len(merge_list)} ta."
        )
        return

    notice = await update.message.reply_text(
        f"🔄 {len(merge_list)} ta PDF birlashtirilmoqda..."
    )

    try:
        merged = pdf_tools.merge_pdfs(merge_list)
    except Exception:
        logger.exception("Merge xatosi")
        await update.message.reply_text("❌ Birlashtirib bo'lmadi.")
        return

    try:
        await update.message.reply_document(
            document=BytesIO(merged),
            filename="merged.pdf",
            caption=f"✅ {len(merge_list)} ta PDF birlashtirildi.",
        )
    except Exception:
        logger.exception("Merge natijasini yuborishda xato")
        await update.message.reply_text("❌ Faylni yuborib bo'lmadi (juda katta bo'lishi mumkin).")
    finally:
        try:
            await notice.delete()
        except Exception:
            pass
        context.user_data["merge_pdfs"] = []
        context.user_data["mode"] = None
