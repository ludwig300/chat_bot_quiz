import json
import os
import random

import redis
import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from quiz_parcer import get_random_question, get_user_score, update_user_score


def send_vk_message(event, vk_api_instance, message, keyboard_str=None):
    vk_api_instance.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000),
        keyboard=keyboard_str
    )


def get_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Новый вопрос"
                },
                "color": "primary"
            }, {
                "action": {
                    "type": "text",
                    "label": "Сдаться"
                },
                "color": "negative"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Мой счет"
                },
                "color": "secondary"
            }]
        ]
    }

    keyboard_str = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    return str(keyboard_str.decode('utf-8'))


if __name__ == "__main__":
    load_dotenv()
    vk_api_token = os.getenv('VK_API_TOKEN')
    vk_session = vk_api.VkApi(token=vk_api_token)
    vk_api_instance = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    # Redis setup
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_password = os.getenv('REDIS_PASSWORD')
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0)

    keyboard_str = get_keyboard()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id

            if event.text == "Новый вопрос":
                question, answer = get_random_question()
                r.set(user_id, answer)
                send_vk_message(event, vk_api_instance, f"Вот ваш новый вопрос: {question}", keyboard_str)

            elif event.text == "Сдаться":
                correct_answer = r.get(user_id)
                if correct_answer:
                    send_vk_message(event, vk_api_instance, f"Вот правильный ответ: {correct_answer.decode('utf-8')}", keyboard_str)
                else:
                    send_vk_message(event, vk_api_instance, "Вы еще не начали игру. Нажмите 'Новый вопрос' для начала.", keyboard_str)

            elif event.text == "Мой счет":
                score = get_user_score(user_id, r)
                send_vk_message(event, vk_api_instance, f"Ваш счет: {score}", keyboard_str)

            else:
                user_answer = event.text.strip().lower()
                correct_answer = r.get(user_id).decode('utf-8').strip().lower()

                if user_answer == correct_answer:
                    update_user_score(user_id, r)
                    send_vk_message(event, vk_api_instance, "Правильно! Поздравляю!", keyboard_str)
                else:
                    send_vk_message(event, vk_api_instance, "Неправильно… Попробуешь ещё раз?", keyboard_str)