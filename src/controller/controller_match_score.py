from src.controller.controller_base import BaseController


class MatchScoreController(BaseController):
    def __init__(
            self,
            service: type,
        ):
        self.service = service