import logging
from result import Result, Ok, Err
from sqlalchemy.exc import SQLAlchemyError

from src.errors import InitialError
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
            player1 = self.dao_players.get_by_name(dto.player1.name)
            if not player1:
                player1 = self.dao_players.insert(dto.player1)
            player2 = self.dao_players.get_by_name(dto.player2.name)
            if not player2:
                player2 = self.dao_players.insert(dto.player2)
            dto.player1.id = player1.id
            dto.player2.id = player2.id

            match = self.dao_mathes.insert(dto)
            dto.uuid = match.uuid
            return Ok(dto)
        except SQLAlchemyError as e:
            logging.debug(f"Ошибка базы данных: {e}")
            return Err(InitialError())
