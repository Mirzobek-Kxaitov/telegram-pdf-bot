import logging
from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from services import pdf_tools
from services.i18n import t

from . import get_lang

logger = logging.getLogger(__name__)

MIN_PASSWORD_LENGTH = 4


async def prompt_set_password(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    if not context.user_data.get("pending_pdf"):
        await query.edit_message_text(t("pdf_not_found", lang))
        return
    context.user_data["mode"] = "awaiting_password_set"
    await query.edit_message_text(t("password_set_prompt", lang, min=MIN_PASSWORD_LENGTH))


async def prompt_remove_password(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, query.from_user)
    if not context.user_data.get("pending_pdf"):
        await query.edit_message_text(t("pdf_not_found", lang))
        return
    context.user_data["mode"] = "awaiting_password_remove"
    await query.edit_message_text(t("password_remove_prompt", lang))


async def _delete_user_message_silently(update: Update):
    try:
        await update.message.delete()
    except Exception:
        pass


def _clear_pending(context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("pending_pdf", None)
    context.user_data.pop("pending_pdf_pages", None)
    context.user_data.pop("pending_pdf_encrypted", None)
    context.user_data["mode"] = None


async def handle_password_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    mode = context.user_data.get("mode")
    password = (update.message.text or "").strip()
    pdf_bytes = context.user_data.get("pending_pdf")
    chat = update.message.chat

    if not pdf_bytes:
        await update.message.reply_text(t("pdf_not_found", lang))
        context.user_data["mode"] = None
        return

    if mode == "awaiting_password_set":
        await _delete_user_message_silently(update)
        if len(password) < MIN_PASSWORD_LENGTH:
            await chat.send_message(t("password_too_short", lang, min=MIN_PASSWORD_LENGTH))
            return

        notice = await chat.send_message(t("setting_password", lang))
        try:
            encrypted = pdf_tools.encrypt_pdf(pdf_bytes, password)
        except Exception:
            logger.exception("PDF shifrlashda xato")
            await chat.send_message(t("encrypt_error", lang))
            return

        try:
            await chat.send_document(
                document=BytesIO(encrypted),
                filename="encrypted.pdf",
                caption=t("password_set_done", lang),
            )
        except Exception:
            logger.exception("Shifrlangan PDF yuborishda xato")
            await chat.send_message(t("send_error", lang))
        finally:
            try:
                await notice.delete()
            except Exception:
                pass
            _clear_pending(context)
        return

    if mode == "awaiting_password_remove":
        await _delete_user_message_silently(update)
        notice = await chat.send_message(t("removing_password", lang))
        try:
            decrypted = pdf_tools.decrypt_pdf(pdf_bytes, password)
        except ValueError:
            try:
                await notice.delete()
            except Exception:
                pass
            await chat.send_message(t("wrong_password", lang))
            return
        except Exception:
            logger.exception("Deshifrlashda xato")
            try:
                await notice.delete()
            except Exception:
                pass
            await chat.send_message(t("decrypt_error", lang))
            return

        try:
            await chat.send_document(
                document=BytesIO(decrypted),
                filename="decrypted.pdf",
                caption=t("password_removed_done", lang),
            )
        except Exception:
            logger.exception("Deshifrlangan PDF yuborishda xato")
            await chat.send_message(t("send_error", lang))
        finally:
            try:
                await notice.delete()
            except Exception:
                pass
            _clear_pending(context)
