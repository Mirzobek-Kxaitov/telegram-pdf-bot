from telegram import Update
from telegram.ext import ContextTypes

from services.i18n import LANG_NAMES, SUPPORTED_LANGS, detect_lang, t

from . import language_keyboard


def _lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    tg_lang = update.effective_user.language_code if update.effective_user else None
    return detect_lang(context.user_data, tg_lang)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saved_lang = context.user_data.get("lang")
    context.user_data.clear()
    if saved_lang:
        context.user_data["lang"] = saved_lang
    lang = _lang(update, context)
    await update.message.reply_text(t("welcome", lang), parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang(update, context)
    await update.message.reply_text(t("help", lang), parse_mode="Markdown")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang(update, context)
    had_state = bool(
        context.user_data.get("images")
        or context.user_data.get("merge_pdfs")
        or context.user_data.get("pending_pdf")
        or context.user_data.get("mode")
    )
    saved_lang = context.user_data.get("lang")
    context.user_data.clear()
    if saved_lang:
        context.user_data["lang"] = saved_lang
    msg = t("cancel_cleared", lang) if had_state else t("cancel_nothing", lang)
    await update.message.reply_text(msg)


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = _lang(update, context)
    await update.message.reply_text(
        t("language_prompt", lang),
        reply_markup=language_keyboard(),
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    code = query.data.split(":", 1)[1] if ":" in query.data else None
    if code not in SUPPORTED_LANGS:
        return
    context.user_data["lang"] = code
    await query.edit_message_text(t("language_set", code, name=LANG_NAMES[code]))
    await query.message.chat.send_message(t("welcome", code), parse_mode="Markdown")
