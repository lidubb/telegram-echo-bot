import os
from datetime import datetime

from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# Постоянная клавиатура
def get_keyboard():
    keyboard = [
        ["👋 Привет", "🕒 Время"],
        ["❓ Помощь"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# Инлайн-клавиатура
def get_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🌐 Перейти на сайт",
                callback_data="website"
            )
        ],
        [
            InlineKeyboardButton(
                "📤 Поделиться",
                callback_data="share"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# Команда START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой Telegram-бот!\n"
        "Выбирай действие с помощью кнопок.",
        reply_markup=get_keyboard()
    )


# Команда HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/menu — главное меню"
    )


# Команда MENU
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "👋 Приветствие",
                callback_data="hello"
            )
        ],
        [
            InlineKeyboardButton(
                "🕒 Время",
                callback_data="time"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 Сайт",
                callback_data="website"
            )
        ]
    ]

    await update.message.reply_text(
        "Главное меню. Выбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Обработка обычных кнопок
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    if text == "👋 Привет":
        await update.message.reply_text("Привет! Рад тебя видеть!")

    elif text == "🕒 Время":
        current_time = datetime.now().strftime("%H:%M:%S")
        await update.message.reply_text(
            f"Текущее время: {current_time}"
        )

    elif text == "❓ Помощь":
        await help_command(update, context)

    else:
        await update.message.reply_text(
            f"Ты написал: {text}"
        )


# Обработка инлайн-кнопок
async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    if query.data == "hello":
        await query.message.reply_text(
            "Привет! Добро пожаловать!"
        )

    elif query.data == "time":
        current_time = datetime.now().strftime("%H:%M:%S")
        await query.message.reply_text(
            f"Сейчас {current_time}"
        )

    elif query.data == "website":
        await query.message.reply_text(
            "Наш сайт: https://www.python.org/"
        )

    elif query.data == "share":
        await query.message.reply_text(
            "Поделись ботом:\n"
            "https://t.me/share/url?url=https://t.me/"
        )


# Эхо-функция
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        update.message.text
    )


# Запуск бота
def main():

    if not TOKEN:
        raise ValueError("Токен не найден!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu))

    app.add_handler(
        CallbackQueryHandler(callback_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.Regex(
                "^(👋 Привет|🕒 Время|❓ Помощь)$"
            ),
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo
        )
    )

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()