import telebot
import dbworker
import config


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





if __name__ == '__main__':
    bot.polling(none_stop=True)