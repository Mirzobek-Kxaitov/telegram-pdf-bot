import logging
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from telegram import Update
from telegram.ext import ContextTypes

from config import (
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    MAX_IMAGES_PER_USER,
    MAX_TOTAL_USER_BYTES,
    MAX_TOTAL_USER_MB,
)
from services.i18n import t

from . import get_lang, send_done_footer, total_user_bytes

logger = logging.getLogger(__name__)


async def _store_image(update: Update, context: ContextTypes.DEFAULT_TYPE, file, size: int | None):
    lang = get_lang(context, update.effective_user)

    if size and size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(t("image_too_large", lang, mb=MAX_FILE_SIZE_MB))
        return

    images = context.user_data.setdefault("images", [])
    if len(images) >= MAX_IMAGES_PER_USER:
        await update.message.reply_text(t("max_images_reached", lang, max=MAX_IMAGES_PER_USER))
        return

    buf = BytesIO()
    await file.download_to_memory(buf)
    data = buf.getvalue()

    if total_user_bytes(context.user_data) + len(data) > MAX_TOTAL_USER_BYTES:
        await update.message.reply_text(t("total_size_exceeded", lang, mb=MAX_TOTAL_USER_MB))
        return

    try:
        Image.open(BytesIO(data)).verify()
    except (UnidentifiedImageError, Exception):
        await update.message.reply_text(t("unsupported_image", lang))
        return

    images.append(data)
    await update.message.reply_text(t("image_received", lang, count=len(images)))


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        await _store_image(update, context, file, photo.file_size)
    except Exception:
        logger.exception("Rasm qabul qilishda xato")
        lang = get_lang(context, update.effective_user)
        await update.message.reply_text(t("photo_error", lang))


async def handle_image_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        document = update.message.document
        if not document.mime_type or not document.mime_type.startswith("image/"):
            lang = get_lang(context, update.effective_user)
            await update.message.reply_text(t("only_images_please", lang))
            return
        file = await context.bot.get_file(document.file_id)
        await _store_image(update, context, file, document.file_size)
    except Exception:
        logger.exception("Hujjat qabul qilishda xato")
        lang = get_lang(context, update.effective_user)
        await update.message.reply_text(t("document_error", lang))


def _parse_reorder(text: str, count: int, lang: str) -> list[int]:
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if not parts:
        raise ValueError(t("reorder_err_empty", lang))
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        raise ValueError(t("reorder_err_chars", lang))
    if len(nums) != count:
        raise ValueError(t("reorder_err_count", lang, expected=count, got=len(nums)))
    if sorted(nums) != list(range(1, count + 1)):
        raise ValueError(t("reorder_err_invalid", lang, max=count))
    return [n - 1 for n in nums]


async def reorder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    images = context.user_data.get("images", [])
    if len(images) < 2:
        await update.message.reply_text(t("reorder_need_two", lang))
        return
    context.user_data["mode"] = "awaiting_reorder"
    example = ",".join(str(i) for i in range(len(images), 0, -1))
    await update.message.reply_text(
        t("reorder_prompt", lang, count=len(images), example=example),
        parse_mode="Markdown",
    )


async def handle_reorder_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    images = context.user_data.get("images", [])
    if not images:
        await update.message.reply_text(t("reorder_no_images", lang))
        context.user_data["mode"] = None
        return

    try:
        new_order = _parse_reorder(update.message.text or "", len(images), lang)
    except ValueError as e:
        await update.message.reply_text(t("reorder_invalid", lang, error=str(e)))
        return

    context.user_data["images"] = [images[i] for i in new_order]
    context.user_data["mode"] = None
    order_str = ",".join(str(i + 1) for i in new_order)
    await update.message.reply_text(t("reorder_done", lang, order=order_str))


def _open_rgb(image_bytes: bytes) -> Image.Image:
    img = Image.open(BytesIO(image_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


async def images_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context, update.effective_user)
    image_bytes_list = context.user_data.get("images", [])
    if not image_bytes_list:
        await update.message.reply_text(t("no_images", lang))
        return

    notice = await update.message.reply_text(
        t("converting_to_pdf", lang, count=len(image_bytes_list))
    )

    pdf_buffer = BytesIO()
    pil_images: list[Image.Image] = []
    try:
        pil_images = [_open_rgb(b) for b in image_bytes_list]
        first, *rest = pil_images
        first.save(
            pdf_buffer,
            format="PDF",
            save_all=True,
            append_images=rest,
        )
        pdf_buffer.seek(0)

        await update.message.reply_document(
            document=pdf_buffer,
            filename="converted.pdf",
            caption=t("pdf_ready", lang, count=len(image_bytes_list)),
        )
    except Exception:
        logger.exception("PDF yasashda xato")
        await update.message.reply_text(t("pdf_generation_error", lang))
    finally:
        for img in pil_images:
            try:
                img.close()
            except Exception:
                pass
        try:
            await notice.delete()
        except Exception:
            pass
        context.user_data["images"] = []
        await send_done_footer(update.effective_chat, lang)
