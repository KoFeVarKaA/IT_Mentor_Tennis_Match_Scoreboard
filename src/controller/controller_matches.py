from src.controller.controller_base import BaseController


class MatchesController(BaseController):
    def __init__(
            self,
            service: type,
        ):
        self.service = service