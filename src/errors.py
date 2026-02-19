class ObjectNotFoundError(Exception):
    def __init__(self, obj: str, field: str | None = None):
        self.message = f"Объект `{obj}` не найден"
        if field:
            self.message += f" со значением `{field}`"

class ObjectAlreadyExists(Exception):
    def __init__(self, obj: str, field: str | None = None):
        self.message = f"Объект `{obj}` уже существует"
        if field:
            self.message += f" со значением `{field}`"

class InitialError(Exception):
    def __init__(self):
        self.message = f"Ошибка сервера. Что то пошло не так"