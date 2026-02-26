import logging
from result import Result, Ok, Err
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.dao.matches.model import Matches
from src.dto.dto_player import PlayerDTO
from src.errors import InitialError
from src.dto.dto_matches import MatchesDTO
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

    def get_matches(self, dto: MatchesDTO)-> Result[MatchesDTO, InitialError]:
        try:
            if dto.filter_by_name: 
                matches = self.dao_mathes.get_matches(
                        player_name=dto.filter_by_name, offset=(dto.page-1)*5, limit=(dto.page-1)*5+5)
                dto.total_matches_count = self.dao_mathes.get_matches_count(
                        player_name=dto.filter_by_name)
            else:
                matches = self.dao_mathes.get_matches(
                                                        offset=(dto.page-1)*5, limit=(dto.page-1)*5+5)
                dto.total_matches_count = self.dao_mathes.get_matches_count()
                
            for match in matches:
                dto.matches.append(self._to_dto(match))
            return Ok(matches)
        except OperationalError as e:
            logging.debug(f"Ошибка базы данных: Проверьте подключение к бд \n {e}")
            return Err(InitialError())
        except SQLAlchemyError as e:
            logging.debug(f"Ошибка базы данных: {e}")
            return Err(InitialError())


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

    def _to_dto(self, match: Matches):
        return MatchDTO(
            id = match.id,
            uuid = match.uuid,
            player1 = PlayerDTO(id = match.player1_obj.id, name=match.player1_obj.name),
            player2 = PlayerDTO(id = match.player2_obj.id, name=match.player2_obj.name),
            winner = (
                PlayerDTO(id = match.winner_obj.id, name=match.winner_obj.name) 
                if match.winner_obj else PlayerDTO()),
            score = match.score,
        )