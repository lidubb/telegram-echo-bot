Telegram Echo Bot

Описание проекта

Простой Telegram-бот, разработанный на Python с использованием библиотеки python-telegram-bot.

Возможности

* /start — приветствие пользователя.
* /help — список доступных команд.
* Эхо-функция — повторяет сообщения пользователя.

Используемые технологии

* Python
* python-telegram-bot
* python-dotenv

Установка

1. Клонировать репозиторий.
2. Создать виртуальное окружение:

python -m venv venv

3. Активировать окружение:

venv\Scripts\activate

4. Установить зависимости:

pip install -r requirements.txt

5. Создать файл .env и добавить токен:

BOT_TOKEN=your_token

6. Запустить бота:

python bot.py