import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_TOKEN
from handlers import done, image_to_pdf, pdf_router, start

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN o'rnatilmagan!")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("help", start.help_command))
    app.add_handler(CommandHandler("cancel", start.cancel))
    app.add_handler(CommandHandler("reset", start.cancel))
    app.add_handler(CommandHandler("done", done.done))

    app.add_handler(MessageHandler(filters.PHOTO, image_to_pdf.handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, image_to_pdf.handle_image_document))
    app.add_handler(MessageHandler(filters.Document.PDF, pdf_router.handle_pdf_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pdf_router.handle_text))

    app.add_handler(CallbackQueryHandler(pdf_router.button_callback))

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
