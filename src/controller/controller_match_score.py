import logging

from src.dto.dto_match import MatchDTO
from src.errors import InitialError
from src.response import Responses
from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController
from src.view.render import Render


class MatchScoreController(BaseController):
    def __init__(
            self,
            service: MatchesService,
            render: Render,
        ):
        self.service = service
        self.render = render

    def do_GET(self, path, query):
        try:
            uuid=query["uuid"][0]

            dto = MatchDTO(
                uuid = uuid
            )
        except KeyError:
            message = "Ошибка ввода. Неправильный формат запроса"
            logging.error(message)
            return Responses.input_err(message=message)

        result = self.service.get_match(dto)

        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)
            
        return Responses.success(data=self.render.render_matches(dto))