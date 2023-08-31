ram_token

# Quiz Bot Project

## Описание

Этот проект включает в себя двух ботов для викторин: одного для VK и одного для Telegram. Боты задают пользователю вопросы, и есть возможность узнать свой текущий счет.

## Требования

* `Python 3.x`
* `python-dotenv==1.0.0`
* `python-telegram-bot==13.15`
* `redis==5.0.0`
* `vk-api==11.9.9`

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/ludwig300/chat_bot_quiz.git

   ```
2. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Установите и запустите Redis.
4. Заполните `.env` файл
   ```
   FILEPATH='path_to_text_file_with_question_and_answer'
   VK_API_TOKEN=your_vk_api_token

   TG_TOKEN=your_telegram_token
   REDIS_HOST=your_redis_host
   REDIS_PORT=your_redis_port
   REDIS_PASSWORD==your_redis_password
   ```

## Использование

### VK Bot

1. Запустите бота:

   ```
   python vk_bot.py
   ```
2. Отправьте сообщение "Новый вопрос" боту в VK для начала викторины.

### Telegram Bot

1. Запустите бота:

   ```
   python tg_bot.py
   ```
2. Отправьте команду `/start` боту в Telegram для начала викторины.

## Функциональность

* Запрос нового вопроса: "Новый вопрос" или `/new_question` в Telegram.
* Сдаться: "Сдаться" или `/give_up` в Telegram.
* Посмотреть свой счет: "Мой счет".
