import logging
from src.dto.dto_error import ErrorDTO
from src.dto.dto_match import MatchDTO
from src.dto.dto_player import PlayerDTO
from src.errors import InitialError
from src.response import Responses
from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController
from src.utils.exception_handlers import handle_key_error
from src.view.render import Render


class MatchNewController(BaseController):
    def __init__(
            self,
            service: MatchesService,
            render: Render,
        ):
        self.service = service
        self.render = render

    @staticmethod
    def do_GET(path, query):
        with open("src/view/static/new-match.html", "rb") as file:
            return {
                "status_code" : 200,
                "data" : file.read()
                }
    
    @handle_key_error
    def do_POST(
            self, 
            path,
            query,
            data: dict,
            ):
        player1_name=data["playerOne"][0]
        player2_name=data["playerTwo"][0]

        if len(player1_name) < 3 or len(player2_name) < 3:
            message="Ошибка ввода. Длина имени игрока должна составлять хотя бы 3 символа"
            logging.error(message)
            return Responses.input_err(self.render.render_error(error_dict=ErrorDTO(
                status_code=400, message=message)))
        elif len(player1_name) >= 45 or len(player2_name) >= 45:
            message="Ошибка ввода. Максимальная длина имени игрока - 45 символов"
            logging.error(message)
            return Responses.input_err(self.render.render_error(error_dict=ErrorDTO(
                status_code=400, message=message)))

        dto = MatchDTO(
            player1 = PlayerDTO(name=player1_name),
            player2 = PlayerDTO(name=player2_name)
        )
        
        result = self.service.post_new_match(dto)

        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                logging.error(f"Ошибка базы данных или сервера")
                return Responses.initial_err(self.render.render_error(error_dict=ErrorDTO(
                    status_code=500, message=result.unwrap_err().message)))
            
        return Responses.redirect(url=f"/match-score?uuid={dto.uuid}")