from dataclasses import dataclass

from src.dto.dto_match import MatchDTO
from src.dao.matches.model import Matches
from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchesDTO():
    page: int
    filter_by_name: str | None
    matches: list[MatchDTO] = None
    total_matches_count: int = None
