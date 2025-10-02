from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import os

# токен берём из Railway переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --------- ДАННЫЕ ---------
# загружаем фразы карт и цитат из файлов
with open("data/ua_cards.txt", "r", encoding="utf-8") as f:
    cards_ua = f.read().splitlines()

with open("data/en_cards.txt", "r", encoding="utf-8") as f:
    cards_en = f.read().splitlines()

with open("data/ua_quotes.txt", "r", encoding="utf-8") as f:
    quotes_ua = f.read().splitlines()

with open("data/en_quotes.txt", "r", encoding="utf-8") as f:
    quotes_en = f.read().splitlines()


# --------- ОБРАБОТЧИКИ ---------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Українська 🇺🇦", callback_data='lang_ua')],
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')]
    ]
    await update.message.reply_text(
        "🌍 Please choose language / Будь ласка, оберіть мову:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # выбор языка
    if query.data == 'lang_ua':
        context.user_data['lang'] = 'ua'
        keyboard = [
            [InlineKeyboardButton("Метафоричні карти", callback_data='cards')],
            [InlineKeyboardButton("Цитата дня", callback_data='quote')]
        ]
        await query.edit_message_text("Оберіть опцію:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'lang_en':
        context.user_data['lang'] = 'en'
        keyboard = [
            [InlineKeyboardButton("Metaphorical Cards", callback_data='cards')],
            [InlineKeyboardButton("Daily Quote", callback_data='quote')]
        ]
        await query.edit_message_text("Choose an option:", reply_markup=InlineKeyboardMarkup(keyboard))

    # выбор карт
    elif query.data == 'cards':
        lang = context.user_data.get('lang', 'en')
        if lang == 'ua':
            cards = cards_ua
        else:
            cards = cards_en

        card_index = random.randint(0, len(cards) - 1)
        card_text = cards[card_index]
        card_image = f"data/images/{card_index+1}.png"   # путь меняем на относительный

        with open(card_image, 'rb') as img:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=img,
                caption=card_text
            )

    # выбор цитаты
    elif query.data == 'quote':
        lang = context.user_data.get('lang', 'en')
        if lang == 'ua':
            quote = random.choice(quotes_ua)
        else:
            quote = random.choice(quotes_en)

        await query.edit_message_text(text=f"✨ {quote}")


# --------- ЗАПУСК ---------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
