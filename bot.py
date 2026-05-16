import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import (
    GET_UPDATES_TIMEOUT,
    NETWORK_CONNECT_TIMEOUT,
    NETWORK_POOL_TIMEOUT,
    NETWORK_READ_TIMEOUT,
    NETWORK_WRITE_TIMEOUT,
    TELEGRAM_TOKEN,
)
from handlers import done, image_to_pdf, pdf_router, start

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN o'rnatilmagan!")

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .read_timeout(NETWORK_READ_TIMEOUT)
        .write_timeout(NETWORK_WRITE_TIMEOUT)
        .connect_timeout(NETWORK_CONNECT_TIMEOUT)
        .pool_timeout(NETWORK_POOL_TIMEOUT)
        .get_updates_read_timeout(GET_UPDATES_TIMEOUT)
        .build()
    )

    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("help", start.help_command))
    app.add_handler(CommandHandler("cancel", start.cancel))
    app.add_handler(CommandHandler("reset", start.cancel))
    app.add_handler(CommandHandler("done", done.done))
    app.add_handler(CommandHandler("reorder", image_to_pdf.reorder_command))
    app.add_handler(CommandHandler("language", start.language_command))

    app.add_handler(MessageHandler(filters.PHOTO, image_to_pdf.handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, image_to_pdf.handle_image_document))
    app.add_handler(MessageHandler(filters.Document.PDF, pdf_router.handle_pdf_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pdf_router.handle_text))

    app.add_handler(CallbackQueryHandler(start.language_callback, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(pdf_router.button_callback))

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
