import functools
import logging

from src.response import Responses

def handle_key_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            message = "Ошибка ввода. Неправильный формат запроса"
            logging.error(message)
            with open("src/view/errors/input_error.html", "rb") as file:
                return {
                    "status_code" : 200,
                    "data" : file.read()
                    }
    return wrapper
