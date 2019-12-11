import telebot
import dbworker
import config
import apiface
import requests
import json
import re
from config import forbidden_messages, offensive_messages


bot = telebot.TeleBot(config.token)


# При введенні команди '/start' привітаємося з користувачем.
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    if (dbworker.get_data(str(message.chat.id) + 'name')):
        bot.send_message(message.chat.id, f"Привіт, {dbworker.get_data(str(message.chat.id) + 'name')}!")
    else: 
        bot.send_message(message.chat.id, "Привіт! Як я можу до тебе звертатись?")
        dbworker.set_data(message.chat.id, config.States.S_ENTER_NAME.value)



# При введенні команди '/set_name' змінимо ім'я користувача.
@bot.message_handler(commands=['set_name'])
def set_name(message):
    bot.send_message(message.chat.id, "Тож, як тебе звати?")
    dbworker.set_data(message.chat.id, config.States.S_ENTER_NAME.value)



# Записуємо ім'я користувача
@bot.message_handler(func=lambda message: dbworker.get_data(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    # В випадку з іменем не будемо нічого перевіряти
    bot.send_message(message.chat.id, "Чудове ім'я, запам'ятаю!")
    dbworker.set_data(str(message.chat.id) + 'name', message.text)
    dbworker.set_data(message.chat.id, config.States.S_START.value)



# При введенні команди '/help' виведемо команди для роботи з ботом.
@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Можливо колись тут появиться документація, але це не точно 🙃 \n' \
                     + '\nCпробуй написати "Повстання машин" 😏 \n'
                     + '\nІ навіть не думай мене ображати 😠')



# При введенні команди '/how_old_am_i' визначимо скільки років людині на фото
@bot.message_handler(commands=['how_old_am_i'])
def funcname(message):
    bot.send_message(message.chat.id, 'Для того, щоб я визначив вік, закинь мені фото на якому одна людина.\n' \
                     + 'Якщо на фото буде декілька людей то я визначу вік випадково для когось одного.')
    # Переводимо користувача в стан надсилання фотографії для визначення віку
    dbworker.set_data(message.chat.id, config.States.S_SEND_PIC_FOR_AGE.value)



# Аналізуємо фото користувача та визначаємо вік людини на фото
@bot.message_handler(content_types=["photo"],
                     func=lambda message: dbworker.get_data(message.chat.id) == config.States.S_SEND_PIC_FOR_AGE.value)
def sending_photo_for_age(message):
    # Те, що це фотографія, ми вже перевірили в хендлері, ніяких додаткових дій не потрібно.
    bot.send_message(message.chat.id, "Чудово! Почекай трішки, я проаналізую фотографію та дам відповідь)")
    
    # Дізнаємось відносний шлях до фото
    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    # Повна URL-адреса фотографії
    url_photo = 'https://api.telegram.org/file/bot' + config.token +  '/' + file_info.file_path
    image = apiface.ClImage(url=url_photo)
    # Отримуємо json-відповідь проаналізованого фото
    response = apiface.model.predict([image])

    # Витягуємо вік з відповіді
    try:
        age = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["age_appearance"]["concepts"][0]["name"]
        # print(f'Людині на фото приблизно {age}')
        bot.send_message(message.chat.id, f'Людині на фото приблизно {age}')
    except:
        bot.send_message(message.chat.id, 'Кумедно, але на фото не людина 🧐')

    # Переводимо користувача в нормальний стан
    dbworker.set_data(message.chat.id, config.States.S_START.value)



# При введенні команди '/random_dog' виведемо випадкове фото чи відео собаки.
@bot.message_handler(commands=['random_dog'])
def random_dog(message):
    r = requests.get(url=config.random_dog_api)
    response = r.json()
    # bot.send_message(message.chat.id, response["url"]) # буде виводитись також посилання
    # bot.send_message(message.chat.id, f'[Random dog]({response["url"]})', parse_mode='markdown')
    extension = response["url"].split('.')[-1]
    # Якщо відео
    if ('mp4' in extension):
        bot.send_video(message.chat.id, response["url"])
    # gif
    elif ('gif' in extension):
        bot.send_video_note(message.chat.id, response["url"])
    # Фото
    else:
        bot.send_photo(message.chat.id, response["url"])



# При введенні користувачем фрази з масиву 'forbidden_messages' з 'config' будемо видаляти його повідомлення
@bot.message_handler(func=lambda message: message.text \
                     and re.sub(r'\s+', ' ', message.text.lower()) in forbidden_messages)
def delete_user_message(message):
    # Видаляємо повідомлення 
    bot.delete_message(message.chat.id, message.message_id)


# Так само видалимо повідомлення якщо воно було змінене
@bot.edited_message_handler(func=lambda message: message.text \
                            and re.sub(r'\s+', ' ', message.text.lower()) in forbidden_messages)
def delete_edited_message(message):
    bot.delete_message(message.chat.id, message.message_id)



# При введенні користувачем образливих слів саме до бота з масиву 'offensive_messages' з 'config' 
# будемо відповідати до нього
@bot.message_handler(func=lambda message: message.text \
                     and re.sub(r'\s+', ' ', message.text.lower()) \
                     in map(lambda x: x + ' бот', offensive_messages))
def offensive_message(message):
    # Розіб'ємо речення на слова
    words = re.sub(r'\s+', ' ', message.text.lower()).split()
    # Повернемо образливе слово
    bot.reply_to(message, f"Сам {words[0]}")


# Так само відповімо на повідомлення яке було змінене
@bot.edited_message_handler(func=lambda message: message.text \
                            and re.sub(r'\s+', ' ', message.text.lower()) \
                            in map(lambda x: x + ' бот', offensive_messages))
def edited_offensive_message(message):
    words = re.sub(r'\s+', ' ', message.text.lower()).split()
    bot.reply_to(message, f"Сам {words[0]}")





if __name__ == '__main__':
    bot.polling(none_stop=True)