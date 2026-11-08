import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой первый Telegram-бот!\n"
        "Отправь мне любое сообщение, и я его повторю.\n"
        "Напиши /help для списка команд."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — список команд"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(user_text)


def main():
    if not TOKEN:
        raise ValueError("Токен не найден! Проверь файл .env")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()