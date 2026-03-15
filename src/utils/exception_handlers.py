import functools
import logging

from result import Err
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.errors import InitialError
from src.dto.dto_error import ErrorDTO
from src.response import Responses
from src.view.render import Render

def handle_key_error(func):
    render = Render()
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            message = "Ошибка ввода. Неправильный формат запроса"
            logging.error(message)
            return Responses.input_err(data=render.render_error(
                error_dict = ErrorDTO(
                    status_code=400,
                    message=message
                )
            ))
    return wrapper

def handle_servise_error(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except OperationalError as e:
                logging.debug(f"Ошибка базы данных: Проверьте подключение к бд \n {e}")
                return Err(InitialError())
            except SQLAlchemyError as e:
                logging.debug(f"Ошибка базы данных: {e}")
                return Err(InitialError())
            except Exception as e:
                logging.debug(f"Ошибка в процессе выполнения программы: {e}")
                return Err(InitialError())
        return wrapper