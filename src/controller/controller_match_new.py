import logging
from src.dto.dto_match import MatchDTO
from src.dto.dto_player import PlayerDTO
from src.errors import InitialError
from src.response import Responses
from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController


class MatchNewController(BaseController):
    def __init__(
            self,
            service: MatchesService,
        ):
        self.service = service

    @staticmethod
    def do_GET(path, query):
        with open("src/view/static/new-match.html", "rb") as file:
            return {
                "status_code" : 200,
                "data" : file.read()
                }
        
    def do_POST(
            self, 
            path,
            data: dict,
            ):
        try:
            player1_name=data["playerOne"][0]
            player2_name=data["playerTwo"][0]

            if len(player1_name) < 3 or len(player2_name) < 3:
                message="Ошибка ввода. Длина имени игрока должна составлять 3 символа"
                logging.error(message)
                return Responses.input_err(message)

            dto = MatchDTO(
                player1 = PlayerDTO(name=player1_name),
                player2 = PlayerDTO(name=player2_name)
            )
        except KeyError:
            logging.error("Ошибка ввода. Отсутствует нужное поле формы")
            return Responses.input_err(
                message="Отсутствует нужное поле формы")
        
        result = self.service.post_new_match(dto)

        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.redirect(url=f"/match-score?uuid={dto.uuid}")