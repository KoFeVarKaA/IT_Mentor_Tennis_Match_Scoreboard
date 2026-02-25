from dataclasses import dataclass, field

from src.dto.dto_match import MatchDTO
from src.dao.matches.model import Matches
from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchesDTO():
    page: int
    filter_by_name: str | None
    matches: list[MatchDTO] = field(default_factory=list)
    total_matches_count: int = None

    def to_dict(self):
        return {
            "page" : self.page,
            "filter_by_name" : self.filter_by_name,
            "matches" : self.matches,
            "total_matches_count" : self.total_matches_count,
        }