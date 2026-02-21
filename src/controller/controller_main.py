from src.controller.controller_base import BaseController


class MainController(BaseController):
    @staticmethod
    def do_GET(path, query):
        with open("src/view/static/index.html", "rb") as file:
            return {
                "status_code" : 200,
                "data" : file.read()
                }
                