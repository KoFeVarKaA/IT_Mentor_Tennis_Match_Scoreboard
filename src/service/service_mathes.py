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
            dto.score_to_score_dict()
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
            dto.score_to_score_dict()
            dto = self._render_score(dto)
            dto.score_dict_to_score()
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
        else:
            logging.debug(f"Ошибка в процессе выполнения программы: {error}")
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
    
    def _render_score(dto: MatchDTO) -> MatchDTO:
        def reset_points():
            dto.score_dict["player1_points"] = 0
            dto.score_dict["player2_points"] = 0

        player = f"player{dto.add_point}"
        opponent = f"player{1 if player == 2 else 2}" 
        points_line = {0 : 15, 15: 30, 30: 40}
        
        # Логика очков
        points1, points2 = dto.score_dict[f"{player}_points"], dto.score_dict[f"{opponent}_points"]

        if points1 in points_line:
            dto.score_dict[f"{player}_points"] = points_line[points1]
            if dto.score_dict[f"{player}_points"] == dto.score_dict[f"{opponent}_points"] == 40:
                dto.score_dict[f"{player}_points"] = dto.score_dict[f"{opponent}_points"] = "Равно"

        elif points1 == 40 or points1 == "Преимущество":
            dto.score_dict[f"{player}_games"] += 1
            reset_points()

        elif points1 == "Равно":
            dto.score_dict[f"{player}_points"] = "Преимущество"
            dto.score_dict[f"{opponent}_points"] = 40

        else: #points1[:9] == "Тай-брейк"
            points1, points2 = int(points1[11: ]) + 1, int(points2[11: ])
            if points1 - points2 == 2:
                dto.score_dict[f"{player}_games"] += 1 
                reset_points()
            dto.score_dict[f"{player}_points"] = f"Тай-брейк, {points1}"
        

        # Логика геймов
        games1, games2 = dto.score_dict[f"{player}_games"], dto.score_dict[f"{opponent}_games"]
        if games1 == games2:
            dto.score_dict[f"{player}_points"] = dto.score_dict[f"{opponent}_points"] = "Тай-брейк, 0"
        elif games1 >= 6:
            if games1 - games2 >= 2:
                dto.score_dict[f"{player}_sets"] += 1
                dto.score_dict["player1_games"] = 0
                dto.score_dict["player2_games"] = 0

        # Логика победы
        if dto.score_dict["player1_sets"] == 2:
            dto.winner = dto.player1
        elif dto.score_dict["player2_sets"] == 2:
            dto.winner = dto.player2

        return dto