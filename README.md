
Анонимный Telegram-бот
======================

Этот бот позволяет анонимно отправлять сообщения администратору.
Админ получает сообщение с уникальным кодом отправителя и может ответить пользователю через инлайн-кнопку.
Бот хранит до 10 последних анонимных пользователей в кэше.

Возможности
-----------
- Пользователь пишет боту → сообщение пересылается админу.
- Админ видит сообщение + кнопку «Ответить».
- Админ нажимает на кнопку → его ответ пересылается анонимному пользователю.
- Поддержка нескольких пользователей одновременно (до 10).

Структура проекта
-----------------
anon_bot/
│── anon_requests_bot.py           # Основной код бота
│── requirements.txt # Зависимости
│── .env             # Переменные окружения (создать вручную)

Установка и запуск
------------------

1. Клонировать проект с GitHub:
   git clone git@github.com:DMatyukhin/anon_requests_bot.git
   cd anon_requests_bot

2. Создать виртуальное окружение:
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows

3. Установить зависимости:
   pip install -r requirements.txt

4. Создать файл .env в корне проекта:
   BOT_TOKEN=1234567890:AAExampleBotToken
   ADMIN_ID=987654321

   - BOT_TOKEN — токен вашего Telegram-бота (получить у @BotFather)
   - ADMIN_ID — ваш Telegram ID (узнать через @userinfobot)

5. Запустить бота:
   python anon_requests_bot.py

Запуск на сервере (Ubuntu)
--------------------------
1. Подключитесь к серверу:
   ssh user@your_server_ip

2. Установите Python и Git:
   sudo apt update && sudo apt install -y python3 python3-venv git

3. Клонируйте проект и установите зависимости (как выше).

4. Запустите бота:
   python anon_requests_bot.py

5. Чтобы бот работал после выхода из SSH, используйте:
   nohup python anon_requests_bot.py &

   или настройте systemd-сервис.

Зависимости
-----------
Указаны в requirements.txt:
- aiogram==3.*
- python-dotenv

Лицензия
--------
MIT — свободное использование и доработка.
