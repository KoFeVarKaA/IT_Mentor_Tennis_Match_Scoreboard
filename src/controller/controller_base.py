from abc import ABC, abstractmethod

class BaseController(ABC):
    @abstractmethod
    def do_GET():
        pass

    @abstractmethod
    def do_POST():
        pass

    @abstractmethod
    def do_PATCH():
        pass
