import os
from enum import Enum

token = os.getenv('TOKEN')
db_file = "database.vdb"


class States(Enum):
    """
    Використовується БД Vedis, в якій всі збережені значения завжди рядки,
    тому і тут будуть використовуватися також рядки (str)
    """
    S_START = "0"  # Початок нового діалогу
    S_ENTER_NAME = "1"
    #S_ENTER_AGE = "2"
    #S_SEND_PIC = "3"