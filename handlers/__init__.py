from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from services.i18n import LANG_NAMES, SUPPORTED_LANGS, detect_lang, t


def total_user_bytes(user_data) -> int:
    """Sum of all bytes stored in user_data (images + pending_pdf + merge_pdfs)."""
    total = 0
    for item in user_data.get("images", []):
        if isinstance(item, (bytes, bytearray)):
            total += len(item)
    for pdf in user_data.get("merge_pdfs", []):
        total += len(pdf)
    pending = user_data.get("pending_pdf")
    if pending:
        total += len(pending)
    return total


def get_lang(context, tg_user=None) -> str:
    """Resolve current language. tg_user: update.effective_user or query.from_user."""
    tg_lang = tg_user.language_code if tg_user else None
    return detect_lang(context.user_data, tg_lang)


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(LANG_NAMES[code], callback_data=f"lang:{code}")]
        for code in SUPPORTED_LANGS
    ])


def done_footer_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("btn_help", lang), callback_data="show_help"),
            InlineKeyboardButton(t("btn_language", lang), callback_data="show_language"),
        ],
    ])


async def send_done_footer(chat, lang: str):
    """Send a 'what next' message with help + language buttons after an operation."""
    try:
        await chat.send_message(
            t("footer_done_hint", lang),
            reply_markup=done_footer_keyboard(lang),
        )
    except Exception:
        pass
