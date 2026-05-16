# 📄 PDF Master Bot

Telegram bot — rasmlar va PDF fayllar bilan ishlash uchun ko'p funksiyali yordamchi.

## 🎯 Funksiyalar

- **📸 Rasm → PDF** — bir nechta rasmni bitta PDF faylga aylantirish
- **📄 PDF → Rasm** — PDF sahifalarini JPG rasmlar sifatida chiqarish
- **✂️ PDF bo'lish** — har sahifa alohida yoki kerakli diapazon (`1-3, 5, 7-9`)
- **➕ PDF birlashtirish** — bir nechta PDF'ni bitta qilish
- **📉 PDF siqish** — fayl hajmini 70-95% gacha kamaytirish
- **🔐 Parol qo'yish / olib tashlash** — PDF'ni shifrlash va deshifrlash
- **🔄 Rasm tartibini o'zgartirish** — PDF yasashdan oldin qayta tartiblash
- **🌐 3 ta til** — O'zbek 🇺🇿 / Русский 🇷🇺 / English 🇬🇧 (avtomatik aniqlash)

## 🛠 Texnologiyalar

- **Python 3.11** + `python-telegram-bot 21.6` (async/await)
- **PyMuPDF** (PDF rendering, compression) + **pypdf** (split, merge, encrypt)
- **Pillow** (rasm qayta ishlash)
- **Docker** + **Fly.io** (production deploy)
- **GitHub Actions** (CI/CD — `main`ga push qilingach avtomatik deploy)

## 💡 Arxitektura

- Modulli tuzilish: [handlers/](handlers/), [services/](services/), alohida i18n moduli
- Inline keyboard'lar bilan zamonaviy UX
- Network timeouts va graceful SIGTERM shutdown
- Foydalanuvchi cheklovlari: 20MB/fayl, 50MB/jami (256MB VM uchun OOM oldini olish)
- Maxfiy ma'lumotlar log'ga yoziladi, foydalanuvchiga umumiy xabar
- Parol xabarlari xavfsizlik uchun avtomatik o'chiriladi

## 🚀 Ishga tushirish

```bash
pip install -r requirements.txt
echo "TELEGRAM_TOKEN=your_token_here" > .env
python bot.py
```

## 🔗 Havolalar

- 🤖 Bot: [@your_bot_username](https://t.me/your_bot_username)
- 📦 GitHub: https://github.com/Mirzobek-Kxaitov/telegram-pdf-bot
