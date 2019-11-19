from dotenv import load_dotenv
import os
import telebot
from SQLighter import SQLighter
import utils
import random
from telebot import types

load_dotenv()

############################################

token = os.getenv('TOKEN')
# shelve_name = os.getenv('SHELVE_NAME')
database_name = os.getenv('DATABASE_NAME')

############################################

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['game'])
def game(message):
    # Підключаємося до БД
    db_worker = SQLighter(database_name)
    # Отримуємо випадковий рядок з БД
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Формуємо розмітку
    markup = utils.generate_markup(row[2], row[3])
    # Відправляємо аудіофайл з варіантами відповідей
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Включаємо "ігровий режим"
    utils.set_user_game(message.chat.id, row[2])
    # Від'єднуємося від БД
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Якщо функція повертає None -> Юзер не в грі
    answer = utils.get_answer_for_user(message.chat.id)
    # answer може бути або текст, або None
    # Якщо None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Заберемо клавіатуру з варіантами відповідей.
        keyboard_hider = types.ReplyKeyboardRemove()
        # Якщо відповідь правильна/неправильна
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        # Видаляємо юзера зі сховища (гра закінчена)
        utils.finish_user_game(message.chat.id)


if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)