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
