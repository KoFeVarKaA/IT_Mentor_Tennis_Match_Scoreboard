from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController


class MatchNewController(BaseController):
    def __init__(
            self,
            service: MatchesService,
        ):
        self.service = service