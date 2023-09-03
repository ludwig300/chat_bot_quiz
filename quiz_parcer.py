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


def get_random_question(quiz):  # Теперь принимает quiz как аргумент
    random_question = random.choice(list(quiz.keys()))
    answer = quiz[random_question]
    return random_question, answer


def get_user_score(user_id, r):
    score = r.get(f"score_{user_id}")
    if score is None:
        return 0
    return int(score.decode('utf-8'))


def update_user_score(user_id, r, increment=1):
    current_score = get_user_score(user_id, r)
    r.set(f"score_{user_id}", current_score + increment)
