from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController


class MainController(BaseController):
    def __init__(
            self,
            service: MatchesService,
        ):
        self.service = service

    def do_GET(self, path, query):
        with open("src/view/static/index.html", "rb") as file:
            return {
                "status_code" : 200,
                "data" : file.read()
                }
                