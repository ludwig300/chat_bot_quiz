import logging
import os

import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

from quiz_parcer import get_random_question, get_user_score, update_user_score

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')
r = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    db=0
)

NEW_QUESTION, CHECK_ANSWER, GIVE_UP = range(3)


def start(update: Update, _: CallbackContext) -> int:
    text = "Добро пожаловать на викторину"
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(text,  reply_markup=reply_markup)
    return NEW_QUESTION


def new_question(update: Update, _: CallbackContext) -> int:
    user_id = update.message.chat_id
    question, answer = get_random_question()
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    r.set(user_id, answer)
    update.message.reply_text(question, reply_markup=reply_markup)
    return CHECK_ANSWER


def check_answer(update: Update, _: CallbackContext) -> int:
    user_id = update.message.chat_id
    user_answer = update.message.text.strip().lower()
    correct_answer = r.get(user_id).decode('utf-8').strip().lower()

    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    if user_answer == correct_answer:
        update_user_score(user_id, r)
        update.message.reply_text(
            "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».",
            reply_markup=reply_markup
        )
        return NEW_QUESTION
    else:
        update.message.reply_text(
            "Неправильно… Попробуешь ещё раз?",
            reply_markup=reply_markup
        )
        return CHECK_ANSWER


def give_up(update: Update, _: CallbackContext) -> int:
    user_id = update.message.chat_id
    correct_answer = r.get(user_id).decode('utf-8').strip().lower()
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    update.message.reply_text(
        f"Правильный ответ: {correct_answer}. Для следующего вопроса нажми «Новый вопрос».",
        reply_markup=reply_markup
    )
    return NEW_QUESTION


def show_score(update: Update, _: CallbackContext) -> int:
    user_id = update.message.chat_id
    score = get_user_score(user_id, r)
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(f"Ваш счет: {score}", reply_markup=reply_markup)
    return NEW_QUESTION


def main():
    tg_token = os.getenv("TG_TOKEN")
    updater = Updater(token=tg_token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NEW_QUESTION: [
                MessageHandler(Filters.regex('^Новый вопрос$'), new_question),
                MessageHandler(Filters.regex('^Сдаться$'), give_up),
                MessageHandler(Filters.regex('^Мой счет$'), show_score),
            ],
            CHECK_ANSWER: [
                MessageHandler(Filters.regex('^Сдаться$'), give_up),
                MessageHandler(Filters.text & ~Filters.command, check_answer),
            ],
        },

        fallbacks=[CommandHandler('cancel', start)],

        allow_reentry=True
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
