from telegram import Update
from telegram.ext import ContextTypes

from services.i18n import t

from . import get_lang, image_to_pdf, pdf_merge


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dispatches /done based on current mode."""
    mode = context.user_data.get("mode")

    if mode == "merging":
        await pdf_merge.do_merge(update, context)
        return

    if context.user_data.get("images"):
        await image_to_pdf.images_to_pdf(update, context)
        return

    lang = get_lang(context, update.effective_user)
    await update.message.reply_text(t("done_nothing", lang))
