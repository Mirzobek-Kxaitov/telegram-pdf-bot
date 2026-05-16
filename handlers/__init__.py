from services.i18n import detect_lang


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
