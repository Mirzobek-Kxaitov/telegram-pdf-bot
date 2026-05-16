"""Simple dict-based i18n. Languages: uz (default), ru, en."""
from typing import Optional

DEFAULT_LANG = "uz"
SUPPORTED_LANGS = ("uz", "ru", "en")

LANG_NAMES = {
    "uz": "🇺🇿 O'zbek",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "uz": {
        # === start.py ===
        "welcome": (
            "👋 Assalomu alaykum!\n\n"
            "🤖 Men PDF bilan ishlovchi botman:\n\n"
            "📸 *Rasm → PDF* — rasmlar yuboring, /done bosing.\n"
            "📄 *PDF amallari* — PDF yuboring, tugmadan tanlang:\n"
            "  • Rasmga aylantirish\n"
            "  • Sahifalarga bo'lish\n"
            "  • Birlashtirish (merge)\n"
            "  • Siqish (compress)\n"
            "  • Parol qo'yish / olib tashlash\n"
            "📝 *Word → PDF* — .docx fayl yuboring, avtomatik PDF qiladi.\n\n"
            "ℹ️ Yordam: /help\n"
            "🌐 Til: /language"
        ),
        "help": (
            "📖 *Yordam*\n\n"
            "📸 *Rasmdan PDF:*\n"
            "Rasm yuboring → /done\n"
            "Tartibni o'zgartirish: /reorder\n\n"
            "📄 *PDF amallari:*\n"
            "PDF fayl yuboring → tugma tanlang:\n"
            "  📷 Rasmga aylantirish\n"
            "  ✂️ Sahifalarga bo'lish (har sahifa yoki diapazon)\n"
            "  ➕ Birlashtirish (boshqa PDF qo'shing va /done bosing)\n"
            "  📉 Siqish (Telegram limitiga moslashtirish)\n"
            "  🔐 Parol qo'yish / olib tashlash\n\n"
            "📝 *Word → PDF:*\n"
            ".docx fayl yuboring — avtomatik PDF qiladi.\n"
            "_Eslatma: kompleks formatlash yo'qolishi mumkin._\n\n"
            "🎯 *Komandalar:*\n"
            "/start — qayta boshlash\n"
            "/done — joriy amalni yakunlash\n"
            "/reorder — rasm tartibini o'zgartirish\n"
            "/cancel — bekor qilish\n"
            "/language — til tanlash\n"
            "/help — yordam\n\n"
            "⚠️ *Cheklovlar:* 20MB / fayl, 50MB / jami, 30 rasm, 10 PDF (merge)"
        ),
        "cancel_cleared": "🗑 Tozalandi. Yangidan boshlashingiz mumkin.",
        "cancel_nothing": "ℹ️ Hech narsa yo'q edi. Rasm yoki PDF yuboring.",
        "language_prompt": "🌐 Tilni tanlang:",
        "language_set": "✅ Til o'zgartirildi: {name}",
        "footer_done_hint": "💡 Yana fayl yuboring yoki tugmadan tanlang.",
        "btn_help": "❓ Yordam",
        "btn_language": "🌐 Til",

        # === image_to_pdf.py ===
        "image_too_large": "❌ Rasm juda katta. Maksimal {mb}MB.",
        "max_images_reached": (
            "⚠️ Maksimal {max} ta rasm yuborildi. "
            "/done bosing yoki /cancel bilan bekor qiling."
        ),
        "total_size_exceeded": (
            "⚠️ Jami {mb}MB limit oshib ketadi. "
            "/done bosing yoki /cancel bilan bekor qiling."
        ),
        "unsupported_image": "❌ Bu rasm formati qo'llab-quvvatlanmaydi.",
        "image_received": "✅ Rasm qabul qilindi ({count} ta)\nYana yuboring yoki /done yozing.",
        "photo_error": "❌ Rasmni qabul qilib bo'lmadi.",
        "document_error": "❌ Faylni qabul qilib bo'lmadi.",
        "only_images_please": "⚠️ Iltimos, faqat rasm yuboring (jpg, png, va h.k.)",
        "no_images": "⚠️ Hech qanday rasm yuborilmagan.\nAvval rasm yuboring, keyin /done bosing.",
        "converting_to_pdf": "🔄 {count} ta rasm PDF'ga aylantirilmoqda...",
        "pdf_ready": "✅ Tayyor! {count} ta rasm bitta PDF qilindi.",
        "pdf_generation_error": "❌ PDF yasashda xato yuz berdi. Iltimos, qayta urinib ko'ring.",
        "reorder_need_two": "⚠️ Tartib o'zgartirish uchun kamida 2 ta rasm kerak.",
        "reorder_prompt": (
            "🔄 Hozir {count} ta rasm bor.\n\n"
            "Yangi tartibni vergul bilan kiriting (1 dan {count} gacha).\n\n"
            "Misol (teskari): `{example}`\n\n"
            "Bekor qilish: /cancel"
        ),
        "reorder_no_images": "⚠️ Rasmlar topilmadi.",
        "reorder_invalid": "❌ {error}\n\nQaytadan urinib ko'ring yoki /cancel.",
        "reorder_done": "✅ Tartib o'zgartirildi: {order}\nEndi /done bosing yoki yana rasm yuboring.",
        "reorder_err_empty": "Bo'sh kiritish",
        "reorder_err_chars": "Faqat raqamlar va vergullar bo'lishi kerak",
        "reorder_err_count": "{expected} ta raqam kerak, siz {got} ta yubordingiz",
        "reorder_err_invalid": "Raqamlar 1 dan {max} gacha bo'lishi va takrorlanmasligi kerak",

        # === pdf_router.py ===
        "pdf_too_large": "❌ PDF juda katta. Maksimal {mb}MB.",
        "pdf_download_error": "❌ PDF faylni yuklab bo'lmadi.",
        "pdf_read_error": "❌ PDF faylni o'qib bo'lmadi. Fayl buzilgan bo'lishi mumkin.",
        "pdf_page_read_error": "❌ PDF faylni o'qib bo'lmadi.",
        "pdf_received": "📄 PDF qabul qilindi ({pages} sahifa).\n\nNima qilamiz?",
        "pdf_back_menu": "📄 PDF ({pages} sahifa). Nima qilamiz?",
        "pdf_encrypted_received": "🔐 PDF parol bilan himoyalangan.\n\nNima qilamiz?",
        "cancelled": "❌ Bekor qilindi.",
        "unknown_action": "⚠️ Noma'lum amal.",
        "btn_pdf2img": "📷 Rasmga aylantirish",
        "btn_split": "✂️ Sahifalarga bo'lish",
        "btn_merge": "➕ Birlashtirish (merge)",
        "btn_compress": "📉 Siqish (compress)",
        "btn_password_set": "🔐 Parol qo'yish",
        "btn_password_remove": "🔓 Parolni olib tashlash",
        "btn_cancel": "❌ Bekor qilish",
        "btn_split_each": "📄 Har sahifa alohida",
        "btn_split_range": "🎯 Diapazon kiritaman",
        "btn_back": "🔙 Orqaga",

        # === pdf_to_image.py ===
        "pdf_not_found": "⚠️ PDF topilmadi. Iltimos, PDF'ni qaytadan yuboring.",
        "converting_pages": "🔄 {pages} ta sahifa rasmga aylantirilmoqda...",
        "pdf2img_error": "❌ PDF'ni rasmga aylantirib bo'lmadi.",
        "images_sent": "✅ {count} ta sahifa yuborildi.",
        "images_as_zip": "✅ {count} ta sahifa rasm sifatida ZIP arxivda.",
        "send_error": "❌ Yuborishda xato.",

        # === pdf_split.py ===
        "split_question": "✂️ PDF ({pages} sahifa) qanday bo'linsin?",
        "splitting_pages": "🔄 {count} ta sahifa ajratilmoqda...",
        "split_error": "❌ PDF'ni bo'lib bo'lmadi.",
        "split_each_done": "✅ {count} ta alohida PDF yuborildi.",
        "range_prompt": (
            "🎯 Diapazonni kiriting (PDF da {pages} ta sahifa):\n\n"
            "Misol:\n"
            "• `1-3` — 1-dan 3-gacha bitta PDF\n"
            "• `1-3, 5-7` — ikkita alohida PDF\n"
            "• `1, 3, 5` — uchta alohida sahifa\n\n"
            "Bekor qilish uchun /cancel"
        ),
        "range_error": "❌ {error}\n\nQaytadan urinib ko'ring yoki /cancel bosing.",
        "splitting_range": "🔄 {count} ta qism ajratilmoqda...",
        "split_range_send_error": "❌ Yuborishda xato.",
        "split_range_processing_error": "❌ Bo'lishda xato yuz berdi.",
        "split_range_done": "✅ {count} ta PDF yuborildi.",

        # === pdf_merge.py ===
        "merge_started": (
            "➕ Birlashtirish boshlandi. Hozir {count} ta PDF tayyor.\n\n"
            "Yana PDF yuboring va keyin /done bosing.\n"
            "Bekor qilish uchun /cancel."
        ),
        "max_pdfs_reached": "⚠️ Maksimal {max} ta PDF. /done bosing.",
        "broken_pdf": "❌ PDF buzilgan ko'rinadi.",
        "pdf_added_to_merge": "✅ Qo'shildi ({count} ta). Yana yuboring yoki /done bosing.",
        "merge_need_two": "⚠️ Birlashtirish uchun kamida 2 ta PDF kerak. Hozir {count} ta.",
        "merging": "🔄 {count} ta PDF birlashtirilmoqda...",
        "merge_error": "❌ Birlashtirib bo'lmadi.",
        "merge_done": "✅ {count} ta PDF birlashtirildi.",
        "merge_send_error": "❌ Faylni yuborib bo'lmadi (juda katta bo'lishi mumkin).",
        "merge_pdf_too_large": "❌ PDF juda katta. Maksimal {mb}MB.",
        "merge_total_exceeded": "⚠️ Jami {mb}MB limit oshib ketadi. /done bosing yoki /cancel.",
        "merge_download_error": "❌ PDF'ni yuklab bo'lmadi.",

        # === pdf_compress.py ===
        "compressing": "🔄 {pages} sahifa siqilmoqda... (bu biroz vaqt olishi mumkin)",
        "compress_error": "❌ Siqishda xato yuz berdi.",
        "already_compressed": "ℹ️ PDF allaqachon yaxshi siqilgan ekan — qo'shimcha siqish foyda bermadi.",
        "compress_done": "✅ Siqildi!\n📄 Asl: {orig}\n📉 Yangi: {new} ({percent}% kam)",

        # === pdf_password.py ===
        "password_set_prompt": (
            "🔐 PDF uchun parolni yuboring (kamida {min} belgi).\n\n"
            "⚠️ Xavfsizlik uchun parolni yuborganingizdan keyin men sizning "
            "xabaringizni o'chirib yuboraman.\n\n"
            "Bekor qilish uchun /cancel."
        ),
        "password_remove_prompt": (
            "🔓 PDF parolini yuboring.\n\n"
            "⚠️ Xavfsizlik uchun parolni yuborganingizdan keyin men sizning "
            "xabaringizni o'chirib yuboraman.\n\n"
            "Bekor qilish uchun /cancel."
        ),
        "password_too_short": (
            "❌ Parol kamida {min} belgi bo'lishi kerak. "
            "Qaytadan yuboring yoki /cancel."
        ),
        "setting_password": "🔄 Parol qo'yilmoqda...",
        "encrypt_error": "❌ Parol qo'yishda xato.",
        "password_set_done": "🔐 Parol o'rnatildi.",
        "removing_password": "🔄 Parol olib tashlanmoqda...",
        "wrong_password": "❌ Noto'g'ri parol. Qaytadan yuboring yoki /cancel.",
        "decrypt_error": "❌ Deshifrlashda xato.",
        "password_removed_done": "🔓 Parol olib tashlandi.",

        # === done.py ===
        "done_nothing": "⚠️ Hech narsa yo'q.\nAvval rasm yoki PDF yuboring.",

        # === docx_to_pdf.py ===
        "docx_too_large": "❌ DOCX juda katta. Maksimal {mb}MB.",
        "docx_converting": "🔄 DOCX → PDF konvertatsiya qilinmoqda...",
        "docx_download_error": "❌ DOCX faylni yuklab bo'lmadi.",
        "docx_convert_error": "❌ Konvertatsiyada xato. Hujjat juda murakkab bo'lishi mumkin yoki .docx formatida emas.",
        "docx_done": "✅ Tayyor!\n\n⚠️ Eslatma: kompleks formatlash (rasm, jadval, maxsus shrift) yo'qolishi mumkin.",
    },

    "ru": {
        # === start.py ===
        "welcome": (
            "👋 Здравствуйте!\n\n"
            "🤖 Я бот для работы с PDF:\n\n"
            "📸 *Изображения → PDF* — отправьте картинки, затем /done.\n"
            "📄 *Действия с PDF* — отправьте PDF и выберите кнопку:\n"
            "  • Извлечь страницы как изображения\n"
            "  • Разделить на страницы\n"
            "  • Объединить (merge)\n"
            "  • Сжать (compress)\n"
            "  • Установить / снять пароль\n"
            "📝 *Word → PDF* — отправьте .docx, автоматически сделаю PDF.\n\n"
            "ℹ️ Помощь: /help\n"
            "🌐 Язык: /language"
        ),
        "help": (
            "📖 *Помощь*\n\n"
            "📸 *Изображения → PDF:*\n"
            "Отправьте изображения → /done\n"
            "Изменить порядок: /reorder\n\n"
            "📄 *Действия с PDF:*\n"
            "Отправьте PDF → выберите кнопку:\n"
            "  📷 Извлечь страницы как изображения\n"
            "  ✂️ Разделить (каждая страница или диапазон)\n"
            "  ➕ Объединить (добавьте PDF и нажмите /done)\n"
            "  📉 Сжать (под лимит Telegram)\n"
            "  🔐 Установить / снять пароль\n\n"
            "📝 *Word → PDF:*\n"
            "Отправьте .docx — автоматически сконвертирую в PDF.\n"
            "_Примечание: сложное форматирование может быть потеряно._\n\n"
            "🎯 *Команды:*\n"
            "/start — начать заново\n"
            "/done — завершить текущее действие\n"
            "/reorder — изменить порядок изображений\n"
            "/cancel — отменить\n"
            "/language — выбрать язык\n"
            "/help — помощь\n\n"
            "⚠️ *Лимиты:* 20МБ/файл, 50МБ/итого, 30 изображений, 10 PDF (merge)"
        ),
        "cancel_cleared": "🗑 Очищено. Можно начать заново.",
        "cancel_nothing": "ℹ️ Ничего не было. Отправьте изображение или PDF.",
        "language_prompt": "🌐 Выберите язык:",
        "language_set": "✅ Язык изменён: {name}",
        "footer_done_hint": "💡 Отправьте ещё файл или выберите кнопку.",
        "btn_help": "❓ Помощь",
        "btn_language": "🌐 Язык",

        # === image_to_pdf.py ===
        "image_too_large": "❌ Изображение слишком большое. Максимум {mb}МБ.",
        "max_images_reached": (
            "⚠️ Достигнут лимит в {max} изображений. "
            "Нажмите /done или /cancel."
        ),
        "total_size_exceeded": (
            "⚠️ Превышен общий лимит в {mb}МБ. "
            "Нажмите /done или /cancel."
        ),
        "unsupported_image": "❌ Формат изображения не поддерживается.",
        "image_received": "✅ Изображение принято ({count}). Отправляйте ещё или /done.",
        "photo_error": "❌ Не удалось принять изображение.",
        "document_error": "❌ Не удалось принять файл.",
        "only_images_please": "⚠️ Пожалуйста, отправляйте только изображения (jpg, png и т.д.)",
        "no_images": "⚠️ Изображения не отправлены.\nСначала отправьте изображения, затем /done.",
        "converting_to_pdf": "🔄 Конвертирую {count} изображений в PDF...",
        "pdf_ready": "✅ Готово! {count} изображений объединены в один PDF.",
        "pdf_generation_error": "❌ Ошибка при создании PDF. Попробуйте ещё раз.",
        "reorder_need_two": "⚠️ Для изменения порядка нужно минимум 2 изображения.",
        "reorder_prompt": (
            "🔄 Сейчас {count} изображений.\n\n"
            "Введите новый порядок через запятую (от 1 до {count}).\n\n"
            "Пример (в обратном порядке): `{example}`\n\n"
            "Отмена: /cancel"
        ),
        "reorder_no_images": "⚠️ Изображения не найдены.",
        "reorder_invalid": "❌ {error}\n\nПопробуйте ещё раз или /cancel.",
        "reorder_done": "✅ Порядок изменён: {order}\nТеперь нажмите /done или отправьте ещё.",
        "reorder_err_empty": "Пустой ввод",
        "reorder_err_chars": "Только цифры и запятые",
        "reorder_err_count": "Нужно {expected} чисел, вы прислали {got}",
        "reorder_err_invalid": "Числа должны быть от 1 до {max} без повторений",

        # === pdf_router.py ===
        "pdf_too_large": "❌ PDF слишком большой. Максимум {mb}МБ.",
        "pdf_download_error": "❌ Не удалось загрузить PDF.",
        "pdf_read_error": "❌ Не удалось прочитать PDF. Возможно, файл повреждён.",
        "pdf_page_read_error": "❌ Не удалось прочитать PDF.",
        "pdf_received": "📄 PDF принят ({pages} стр.).\n\nЧто будем делать?",
        "pdf_back_menu": "📄 PDF ({pages} стр.). Что будем делать?",
        "pdf_encrypted_received": "🔐 PDF защищён паролем.\n\nЧто будем делать?",
        "cancelled": "❌ Отменено.",
        "unknown_action": "⚠️ Неизвестное действие.",
        "btn_pdf2img": "📷 В изображения",
        "btn_split": "✂️ Разделить",
        "btn_merge": "➕ Объединить (merge)",
        "btn_compress": "📉 Сжать (compress)",
        "btn_password_set": "🔐 Установить пароль",
        "btn_password_remove": "🔓 Снять пароль",
        "btn_cancel": "❌ Отмена",
        "btn_split_each": "📄 Каждая страница отдельно",
        "btn_split_range": "🎯 Указать диапазон",
        "btn_back": "🔙 Назад",

        # === pdf_to_image.py ===
        "pdf_not_found": "⚠️ PDF не найден. Отправьте PDF заново.",
        "converting_pages": "🔄 Конвертирую {pages} страниц в изображения...",
        "pdf2img_error": "❌ Не удалось конвертировать PDF в изображения.",
        "images_sent": "✅ Отправлено {count} страниц.",
        "images_as_zip": "✅ {count} страниц в виде ZIP-архива.",
        "send_error": "❌ Ошибка при отправке.",

        # === pdf_split.py ===
        "split_question": "✂️ Как разделить PDF ({pages} стр.)?",
        "splitting_pages": "🔄 Разделяю {count} страниц...",
        "split_error": "❌ Не удалось разделить PDF.",
        "split_each_done": "✅ Отправлено {count} отдельных PDF.",
        "range_prompt": (
            "🎯 Введите диапазон (в PDF {pages} стр.):\n\n"
            "Примеры:\n"
            "• `1-3` — один PDF со стр. 1-3\n"
            "• `1-3, 5-7` — два отдельных PDF\n"
            "• `1, 3, 5` — три отдельных страницы\n\n"
            "Отмена: /cancel"
        ),
        "range_error": "❌ {error}\n\nПопробуйте ещё раз или /cancel.",
        "splitting_range": "🔄 Разделяю на {count} частей...",
        "split_range_send_error": "❌ Ошибка при отправке.",
        "split_range_processing_error": "❌ Ошибка при разделении.",
        "split_range_done": "✅ Отправлено {count} PDF.",

        # === pdf_merge.py ===
        "merge_started": (
            "➕ Объединение начато. Готово {count} PDF.\n\n"
            "Отправьте ещё PDF и нажмите /done.\n"
            "Отмена: /cancel."
        ),
        "max_pdfs_reached": "⚠️ Максимум {max} PDF. Нажмите /done.",
        "broken_pdf": "❌ PDF выглядит повреждённым.",
        "pdf_added_to_merge": "✅ Добавлено ({count}). Отправляйте ещё или /done.",
        "merge_need_two": "⚠️ Для объединения нужно минимум 2 PDF. Сейчас {count}.",
        "merging": "🔄 Объединяю {count} PDF...",
        "merge_error": "❌ Не удалось объединить.",
        "merge_done": "✅ Объединено {count} PDF.",
        "merge_send_error": "❌ Не удалось отправить файл (возможно, слишком большой).",
        "merge_pdf_too_large": "❌ PDF слишком большой. Максимум {mb}МБ.",
        "merge_total_exceeded": "⚠️ Превышен лимит в {mb}МБ. /done или /cancel.",
        "merge_download_error": "❌ Не удалось загрузить PDF.",

        # === pdf_compress.py ===
        "compressing": "🔄 Сжимаю {pages} страниц... (может занять время)",
        "compress_error": "❌ Ошибка при сжатии.",
        "already_compressed": "ℹ️ PDF уже хорошо сжат — дополнительное сжатие не помогло.",
        "compress_done": "✅ Сжато!\n📄 Было: {orig}\n📉 Стало: {new} (-{percent}%)",

        # === pdf_password.py ===
        "password_set_prompt": (
            "🔐 Отправьте пароль для PDF (минимум {min} символов).\n\n"
            "⚠️ В целях безопасности ваше сообщение с паролем будет удалено.\n\n"
            "Отмена: /cancel."
        ),
        "password_remove_prompt": (
            "🔓 Отправьте пароль от PDF.\n\n"
            "⚠️ В целях безопасности ваше сообщение с паролем будет удалено.\n\n"
            "Отмена: /cancel."
        ),
        "password_too_short": (
            "❌ Пароль должен быть минимум {min} символов. "
            "Отправьте ещё раз или /cancel."
        ),
        "setting_password": "🔄 Устанавливаю пароль...",
        "encrypt_error": "❌ Ошибка при установке пароля.",
        "password_set_done": "🔐 Пароль установлен.",
        "removing_password": "🔄 Снимаю пароль...",
        "wrong_password": "❌ Неверный пароль. Попробуйте ещё раз или /cancel.",
        "decrypt_error": "❌ Ошибка при расшифровке.",
        "password_removed_done": "🔓 Пароль снят.",

        # === done.py ===
        "done_nothing": "⚠️ Ничего нет.\nСначала отправьте изображение или PDF.",

        # === docx_to_pdf.py ===
        "docx_too_large": "❌ DOCX слишком большой. Максимум {mb}МБ.",
        "docx_converting": "🔄 Конвертирую DOCX → PDF...",
        "docx_download_error": "❌ Не удалось загрузить DOCX.",
        "docx_convert_error": "❌ Ошибка конвертации. Документ слишком сложный или не в формате .docx.",
        "docx_done": "✅ Готово!\n\n⚠️ Внимание: сложное форматирование (изображения, таблицы, нестандартные шрифты) может быть потеряно.",
    },

    "en": {
        # === start.py ===
        "welcome": (
            "👋 Hello!\n\n"
            "🤖 I'm a PDF utility bot:\n\n"
            "📸 *Images → PDF* — send images, then /done.\n"
            "📄 *PDF actions* — send a PDF and pick a button:\n"
            "  • Convert pages to images\n"
            "  • Split into pages\n"
            "  • Merge multiple PDFs\n"
            "  • Compress\n"
            "  • Set / remove password\n"
            "📝 *Word → PDF* — send a .docx, auto-converts to PDF.\n\n"
            "ℹ️ Help: /help\n"
            "🌐 Language: /language"
        ),
        "help": (
            "📖 *Help*\n\n"
            "📸 *Images → PDF:*\n"
            "Send images → /done\n"
            "Reorder: /reorder\n\n"
            "📄 *PDF actions:*\n"
            "Send a PDF → pick a button:\n"
            "  📷 Convert pages to images\n"
            "  ✂️ Split (each page or custom range)\n"
            "  ➕ Merge (add more PDFs and press /done)\n"
            "  📉 Compress (fit Telegram limit)\n"
            "  🔐 Set / remove password\n\n"
            "📝 *Word → PDF:*\n"
            "Send a .docx — auto-converts to PDF.\n"
            "_Note: complex formatting may be lost._\n\n"
            "🎯 *Commands:*\n"
            "/start — restart\n"
            "/done — finish current action\n"
            "/reorder — reorder images\n"
            "/cancel — cancel\n"
            "/language — choose language\n"
            "/help — help\n\n"
            "⚠️ *Limits:* 20MB/file, 50MB total, 30 images, 10 PDFs (merge)"
        ),
        "cancel_cleared": "🗑 Cleared. You can start over.",
        "cancel_nothing": "ℹ️ Nothing to clear. Send an image or PDF.",
        "language_prompt": "🌐 Choose language:",
        "language_set": "✅ Language changed to: {name}",
        "footer_done_hint": "💡 Send another file or pick a button.",
        "btn_help": "❓ Help",
        "btn_language": "🌐 Language",

        # === image_to_pdf.py ===
        "image_too_large": "❌ Image is too large. Maximum {mb}MB.",
        "max_images_reached": (
            "⚠️ Reached the limit of {max} images. "
            "Press /done or /cancel."
        ),
        "total_size_exceeded": (
            "⚠️ Total size limit of {mb}MB would be exceeded. "
            "Press /done or /cancel."
        ),
        "unsupported_image": "❌ This image format is not supported.",
        "image_received": "✅ Image received ({count}). Send more or /done.",
        "photo_error": "❌ Failed to receive the image.",
        "document_error": "❌ Failed to receive the file.",
        "only_images_please": "⚠️ Please send images only (jpg, png, etc.).",
        "no_images": "⚠️ No images sent.\nSend images first, then /done.",
        "converting_to_pdf": "🔄 Converting {count} images to PDF...",
        "pdf_ready": "✅ Done! {count} images merged into one PDF.",
        "pdf_generation_error": "❌ PDF generation failed. Please try again.",
        "reorder_need_two": "⚠️ Reordering needs at least 2 images.",
        "reorder_prompt": (
            "🔄 You have {count} images.\n\n"
            "Enter the new order, comma-separated (1 to {count}).\n\n"
            "Example (reversed): `{example}`\n\n"
            "Cancel: /cancel"
        ),
        "reorder_no_images": "⚠️ No images found.",
        "reorder_invalid": "❌ {error}\n\nTry again or /cancel.",
        "reorder_done": "✅ Order changed: {order}\nPress /done or send more images.",
        "reorder_err_empty": "Empty input",
        "reorder_err_chars": "Only digits and commas allowed",
        "reorder_err_count": "Need {expected} numbers, got {got}",
        "reorder_err_invalid": "Numbers must be 1 to {max} without duplicates",

        # === pdf_router.py ===
        "pdf_too_large": "❌ PDF is too large. Maximum {mb}MB.",
        "pdf_download_error": "❌ Failed to download the PDF.",
        "pdf_read_error": "❌ Failed to read the PDF. The file may be corrupted.",
        "pdf_page_read_error": "❌ Failed to read the PDF.",
        "pdf_received": "📄 PDF received ({pages} pages).\n\nWhat shall we do?",
        "pdf_back_menu": "📄 PDF ({pages} pages). What shall we do?",
        "pdf_encrypted_received": "🔐 PDF is password-protected.\n\nWhat shall we do?",
        "cancelled": "❌ Cancelled.",
        "unknown_action": "⚠️ Unknown action.",
        "btn_pdf2img": "📷 Convert to images",
        "btn_split": "✂️ Split pages",
        "btn_merge": "➕ Merge",
        "btn_compress": "📉 Compress",
        "btn_password_set": "🔐 Set password",
        "btn_password_remove": "🔓 Remove password",
        "btn_cancel": "❌ Cancel",
        "btn_split_each": "📄 Each page separately",
        "btn_split_range": "🎯 Specify range",
        "btn_back": "🔙 Back",

        # === pdf_to_image.py ===
        "pdf_not_found": "⚠️ PDF not found. Please send the PDF again.",
        "converting_pages": "🔄 Converting {pages} pages to images...",
        "pdf2img_error": "❌ Failed to convert PDF to images.",
        "images_sent": "✅ Sent {count} pages.",
        "images_as_zip": "✅ {count} pages as a ZIP archive.",
        "send_error": "❌ Failed to send.",

        # === pdf_split.py ===
        "split_question": "✂️ How should the PDF ({pages} pages) be split?",
        "splitting_pages": "🔄 Splitting {count} pages...",
        "split_error": "❌ Failed to split the PDF.",
        "split_each_done": "✅ Sent {count} separate PDFs.",
        "range_prompt": (
            "🎯 Enter the range (PDF has {pages} pages):\n\n"
            "Examples:\n"
            "• `1-3` — one PDF with pages 1-3\n"
            "• `1-3, 5-7` — two separate PDFs\n"
            "• `1, 3, 5` — three single pages\n\n"
            "Cancel: /cancel"
        ),
        "range_error": "❌ {error}\n\nTry again or /cancel.",
        "splitting_range": "🔄 Splitting into {count} parts...",
        "split_range_send_error": "❌ Failed to send.",
        "split_range_processing_error": "❌ Splitting failed.",
        "split_range_done": "✅ Sent {count} PDFs.",

        # === pdf_merge.py ===
        "merge_started": (
            "➕ Merge started. {count} PDF ready.\n\n"
            "Send more PDFs and press /done.\n"
            "Cancel: /cancel."
        ),
        "max_pdfs_reached": "⚠️ Maximum {max} PDFs. Press /done.",
        "broken_pdf": "❌ PDF appears to be broken.",
        "pdf_added_to_merge": "✅ Added ({count}). Send more or /done.",
        "merge_need_two": "⚠️ Merge needs at least 2 PDFs. You have {count}.",
        "merging": "🔄 Merging {count} PDFs...",
        "merge_error": "❌ Merge failed.",
        "merge_done": "✅ Merged {count} PDFs.",
        "merge_send_error": "❌ Failed to send (file may be too large).",
        "merge_pdf_too_large": "❌ PDF is too large. Maximum {mb}MB.",
        "merge_total_exceeded": "⚠️ Total limit of {mb}MB would be exceeded. /done or /cancel.",
        "merge_download_error": "❌ Failed to download the PDF.",

        # === pdf_compress.py ===
        "compressing": "🔄 Compressing {pages} pages... (this may take a while)",
        "compress_error": "❌ Compression failed.",
        "already_compressed": "ℹ️ PDF is already well-compressed — no further reduction.",
        "compress_done": "✅ Compressed!\n📄 Before: {orig}\n📉 After: {new} (-{percent}%)",

        # === pdf_password.py ===
        "password_set_prompt": (
            "🔐 Send the password for the PDF (at least {min} chars).\n\n"
            "⚠️ For security, your password message will be deleted.\n\n"
            "Cancel: /cancel."
        ),
        "password_remove_prompt": (
            "🔓 Send the PDF password.\n\n"
            "⚠️ For security, your password message will be deleted.\n\n"
            "Cancel: /cancel."
        ),
        "password_too_short": (
            "❌ Password must be at least {min} chars. "
            "Send again or /cancel."
        ),
        "setting_password": "🔄 Setting password...",
        "encrypt_error": "❌ Failed to set password.",
        "password_set_done": "🔐 Password set.",
        "removing_password": "🔄 Removing password...",
        "wrong_password": "❌ Wrong password. Try again or /cancel.",
        "decrypt_error": "❌ Decryption failed.",
        "password_removed_done": "🔓 Password removed.",

        # === done.py ===
        "done_nothing": "⚠️ Nothing here.\nSend an image or PDF first.",

        # === docx_to_pdf.py ===
        "docx_too_large": "❌ DOCX is too large. Maximum {mb}MB.",
        "docx_converting": "🔄 Converting DOCX → PDF...",
        "docx_download_error": "❌ Failed to download DOCX.",
        "docx_convert_error": "❌ Conversion failed. The document may be too complex or not in .docx format.",
        "docx_done": "✅ Done!\n\n⚠️ Note: complex formatting (images, tables, special fonts) may be lost.",
    },
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """Translate `key` to `lang`. Falls back to default lang, then to key itself."""
    catalog = TRANSLATIONS.get(lang) or TRANSLATIONS[DEFAULT_LANG]
    text = catalog.get(key) or TRANSLATIONS[DEFAULT_LANG].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def detect_lang(user_data: dict, telegram_user_lang: Optional[str] = None) -> str:
    """Get current user lang. Priority: stored choice → Telegram hint → default."""
    saved = user_data.get("lang")
    if saved in SUPPORTED_LANGS:
        return saved
    if telegram_user_lang:
        short = telegram_user_lang.split("-")[0].lower()
        if short in SUPPORTED_LANGS:
            return short
    return DEFAULT_LANG
