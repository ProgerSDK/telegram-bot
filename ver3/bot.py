import telebot
import dbworker
import config
import apiface


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
    bot.send_message(message.chat.id, 'Можливо колись тут появиться документація, але це не точно, 🙃')


# При введенні команди '/how_old_am_i' визначимо скільки років людині на фото
@bot.message_handler(commands=['how_old_am_i'])
def funcname(message):
    bot.send_message(message.chat.id, 'Для того, щоб я визначив вік, закинь мені фото на якому одна людина')
    dbworker.set_data(message.chat.id, config.States.S_SEND_PIC_FOR_AGE.value)


# Аналізуємо фото користувача та визначаємо вік людини на фото
@bot.message_handler(content_types=["photo"],
                     func=lambda message: dbworker.get_data(message.chat.id) == config.States.S_SEND_PIC_FOR_AGE.value)
def sending_photo_for_age(message):
    # Те, що це фотографія, ми вже перевірили в хендлері, ніяких додаткових дій не потрібно.
    bot.send_message(message.chat.id, "Чудово! Почекай трішки, я проаналізую фотографію та дам відповідь)")
    
    # response = apiface.model.predict_by_filename('example.jpg')
    response = apiface.model.predict_by_filename(message.photo['file_id'])

    age = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["age_appearance"]["concepts"][0]["name"]
    print(f'Людині на фото приблизно {age}')
    bot.send_message(message.chat.id, f'Людині на фото приблизно {age}')

    dbworker.set_state(message.chat.id, config.States.S_START.value)


if __name__ == '__main__':
    bot.polling(none_stop=True)