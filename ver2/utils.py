import shelve
from SQLighter import SQLighter
from dotenv import load_dotenv
import os
from random import shuffle
import telebot
from telebot import types


shelve_name = os.getenv('SHELVE_NAME')
database_name = os.getenv('DATABASE_NAME')


def count_rows():
    """
    Даний метод рахує загальну кількість рядків в базі даних і зберігає в сховище.
    Потім з цієї кількості будемо вибирати музику.
    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    """
    Отримує зі сховища кількість рядків в БД
     (int) Число рядків
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    """
    Записуємо юзера в гравці і запам'ятовуємо, що він повинен відповісти.
    :param chat_id: id юзера
    :param estimated_answer: правильна відповідь (з БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    """
    Закінчуємо гру поточного користувача і удаляємо правильну відповідь з сховища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    """
    Отримуємо правильну відповідь для поточного користувача.
    В випадку, якщо юзер просто ввів якісь символи, не почавши гру, вертаємо None
    :param chat_id: id юзера
     (str) Правильна відповідь / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Якщо юзер не грає, нічого не вертаємо
        except KeyError:
            return None



def generate_markup(right_answer, wrong_answers):
    """
    Створюємо кастомну клавіатуру для вибору відповіді
    :param right_answer: Правильна відповідь
    :param wrong_answers: Набір неправильних відповідей
     Об'єкт кастомної клавіатури
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеюємо правильну відповідь з неправильними
    all_answers = '{},{}'.format(right_answer, wrong_answers)
    # Створюємо ліст (массив) і записуємо в ньго всі елементи
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    # Добре перемішаємо всі елементи
    shuffle(list_items)
    # Заповнюємо розмітку перемішаними елементами
    for item in list_items:
        markup.add(item)
    return markup
