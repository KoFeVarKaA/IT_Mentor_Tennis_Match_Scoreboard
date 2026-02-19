from src.controller.controller_base import BaseController


class MatchNewConroller(BaseController):
    def __init__(
            self,
            service: type,
        ):
        self.service = service