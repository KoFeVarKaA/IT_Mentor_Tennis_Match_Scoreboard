import logging
from result import Result, Ok, Err
from sqlalchemy.exc import SQLAlchemyError

from src.errors import InitialError, ObjectAlreadyExists
from src.dto.dto_match import MatchDTO
from src.dao.matches.repository import MatchesRepository
from src.dao.players.repository import PlayersRepository


class MatchesService():
    def __init__(
            self,
            repository_mathes: MatchesRepository,
            repository_players: PlayersRepository,
    ):
        self.dao_mathes = repository_mathes
        self.dao_players = repository_players

    def post_new_match(self, dto: MatchDTO) -> Result[MatchDTO, InitialError]:
        try:
            id = self.dao_players.get_by_name(dto.player1.name)
            if not id:
                self.dao_players.post(dto.player1)

            id = self.dao_players.get_by_name(dto.player1.name)
            if not id:
                self.dao_players.post(dto.player1)
        
        except SQLAlchemyError as e:
            logging.debug(f"Ошибка: {e}")
            return Err(InitialError())
