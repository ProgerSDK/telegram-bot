from vedis import Vedis
import config


def set_data(key,value):
    """
    Запис нових даних в базу.
    """
    with Vedis(config.db_file) as db:
        try:
            db[key] = value
            return True
        except:
            # тут бажано обробити ситуацію
            return False


def get_data(key):
    """
    Отримання даних з бази.
    """
    with Vedis(config.db_file) as db:
        try:
            return db[key].decode() # Якщо використовуєтьcя Vedis версії нижче, ніж 0.7.1, то .decode() НЕ ПОТРІБЕН
        except KeyError:  # Якщо такого ключа не виявилось
            # return config.States.S_START.value  # значення по замовчуванню - початок діалогу
            return False