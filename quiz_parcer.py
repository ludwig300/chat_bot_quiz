import random
import re


def get_quiz(filepath):
    with open(filepath, 'r', encoding='KOI8-R') as file:
        file_contents = file.read()
    chunks = file_contents.split('\n\n')
    questions = list()
    answers = list()
    for chunk in chunks:
        if 'Вопрос' in chunk:
            questions.append(chunk)
        elif 'Ответ' in chunk:
            answers.append(chunk)
    quiz = dict()
    for index, question in enumerate(questions):
        key = re.sub(r'\n?Вопрос \d+:\n', '', question)
        value = re.sub(r'\n?Ответ:\n', '', answers[index])
        quiz[key] = value
    return quiz


def get_random_question(quiz):
    random_question = random.choice(list(quiz.keys()))
    answer = quiz[random_question]
    return random_question, answer
