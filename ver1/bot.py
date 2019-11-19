from dotenv import load_dotenv
import os
import telebot

load_dotenv()

############################################

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN) 

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Назва функції не грає ніякої ролі, в принципі
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.polling(none_stop=True)