import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Привет! Я эхо-бот. Напишите мне что-нибудь, и я отвечу тем же.")


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()
    TOKEN = os.getenv("TG_TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()