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

    def get_match(self, dto: MatchDTO)-> Result[MatchDTO, InitialError]:
        try:
            dto = self._to_dto(self.dao_mathes.get_match(dto.uuid))
            dto.score_dict = self._score_to_score_dict(dto.score)
            return Ok(dto)
        
        except Exception as e:
            return self._error_processing(e)
        
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
            return Ok(dto)
        except Exception as e:
            return self._error_processing(e)
        
    def post_match_score(self, dto: MatchDTO) -> Result[MatchDTO, InitialError]:
        try:
            dto = self._to_dto(self.dao_mathes.get_match(dto.uuid))
            dto.score_dict = self._score_to_score_dict(dto.score)
            # dto = self._render_score(dto)
            
            
            dto.score = self._score_dict_to_score(dto.score_dict)
            dto = self.dao_mathes.update_score(dto)
            return Ok(dto)
        except Exception as e:
            return self._error_processing(e)


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
        except Exception as e:
            return self._error_processing(e)


    def _error_processing(self, error: Exception):
        if isinstance(error, OperationalError):
            logging.debug(f"Ошибка базы данных: Проверьте подключение к бд \n {error}")
            return Err(InitialError())
        elif isinstance(error, SQLAlchemyError):
            logging.debug(f"Ошибка базы данных: {error}")
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
    
    def _score_to_score_dict(score: str) -> dict:
        score_split = [score.split(" ")[0].split(":"), score.split(" ")[0].split(":")]
        return {
            "player1_sets" : score_split[0][0],
            "player1_games" : score_split[0][1],
            "player1_points" : score_split[0][2],
            "player2_sets" : score_split[1][0],
            "player2_games" : score_split[1][1],
            "player2_points" : score_split[1][2],
        }

    def _score_dict_to_score(score_dict: dict) -> str:
        return (f"{score_dict["player1_sets"]}:{score_dict["player1_games"]}:{score_dict["player1_points"]} " +
                f"{score_dict["player2_sets"]}:{score_dict["player2_games"]}:{score_dict["player2_points"]}")