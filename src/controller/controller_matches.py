import logging
from math import ceil

from src.dto.dto_error import ErrorDTO
from src.dto.dto_matches import MatchesDTO
from src.errors import InitialError
from src.response import Responses
from src.service.service_mathes import MatchesService
from src.controller.controller_base import BaseController
from src.view.render import Render
from src.utils.exception_handlers import handle_key_error


class MatchesController(BaseController):
    def __init__(
            self,
            service: MatchesService,
            render: Render,
        ):
        self.service = service
        self.render = render

    @handle_key_error
    def do_GET(self, path, query):
        page=query["page"][0]
        if "filter_by_name" in query:
            filter_by_name=query["filter_by_name"][0]
        else:
            filter_by_name=None
        
        for letter in page:
            if letter not in "0123456789":
                message = "Ошибка ввода. Некорректный номер страницы"
                logging.error(message)
                return Responses.input_err(self.render.render_error(error_dict=ErrorDTO(
                    status_code=400, message=message)))
        page = int(page)
        if page == 0:
            url = "/matches?page=1"
            logging.debug(f"Редирект на {url}")
            return Responses.redirect(url=url)

        dto = MatchesDTO(
            page=page,
            filter_by_name=filter_by_name
        )
       
        result = self.service.get_matches(dto)

        if result.is_err():
            if isinstance(result.unwrap_err(), InitialError):
                return Responses.initial_err(self.render.render_error(error_dict=ErrorDTO(
                    status_code=500, message=result.unwrap_err().message)))
            
        total_pages = ceil(dto.total_matches_count / 5)
        if dto.page > total_pages:
            url = f"/matches?page={total_pages}"
            logging.debug(f"Редирект на {url}")
            return Responses.redirect(url=url)
        
        dto.total_pages = (dto.total_matches_count + 4) // 5
        dto.start_page = max(1, dto.page - 2)
        dto.end_page = min(dto.total_pages, dto.start_page + 4)
        if dto.end_page - dto.start_page < 4 and dto.total_pages >= 5:
            dto.start_page = max(1, dto.total_pages - 4)
            dto.end_page = dto.total_pages
        return Responses.success(data=self.render.render_matches(dto))
    