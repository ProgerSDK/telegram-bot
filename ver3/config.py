import os
from enum import Enum


token = os.getenv('TELEGRAM_TOKEN')
db_file = "database.vdb"
clarifai_api_key = os.getenv('CLARIFAI_API_KEY')
random_dog_api = 'https://random.dog/woof.json'


# Повідомлення для видалення (Заборонені)
forbidden_messages = ["повстання машин"]
offensive_messages = ["поганий", "тупий", "нефункціональний"]


class States(Enum):
    """
    Використовується БД Vedis, в якій всі збережені значения завжди рядки,
    тому і тут будуть використовуватися також рядки (str)
    """
    S_START = "0"  # Початок нового діалогу
    S_ENTER_NAME = "1"  # Введення імені користувача
    S_SEND_PIC_FOR_AGE = "2"  # Введення фото для визначення віку
    #S_ENTER_AGE = "3"