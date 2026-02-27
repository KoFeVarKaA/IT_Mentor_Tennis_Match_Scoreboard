import logging

from src.dto.dto_matches import MatchesDTO
from src.errors import InitialError
from src.response import Responses
from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController
from src.view.render import Render


class MatchesController(BaseController):
    def __init__(
            self,
            service: MatchesService,
            render: Render,
        ):
        self.service = service
        self.render = render

    def do_GET(self, path, query):
        try:
            page=int(query["page"][0])
            if "filter_by_name" in query:
                filter_by_name=query["filter_by_name"][0]
            else:
                filter_by_name=None

            dto = MatchesDTO(
                page=page,
                filter_by_name=filter_by_name
            )
        except KeyError:
            message = "Ошибка ввода. Неправильный формат запроса"
            logging.error(message)
            return Responses.input_err(message=message)

        result = self.service.get_matches(dto)

        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(result.unwrap_err().message)

        return Responses.success(data=self.render.render_matches(dto))
    