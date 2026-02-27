from dataclasses import dataclass, field

from src.dao.matches.model import Matches
from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchDTO():
    id : int = None
    uuid : str = None
    player1 : PlayerDTO = PlayerDTO()
    player2 : PlayerDTO = PlayerDTO()
    winner : PlayerDTO = PlayerDTO()
    score : str = "0:0:0 0:0:0"
    score_dict: dict[str: int] = field(default_factory=lambda: {
    "player1_sets": 0,
    "player1_games": 0,
    "player1_points": 0,
    "player2_sets": 0,
    "player2_games": 0,
    "player2_points": 0,
})

    def into_model(self) -> Matches:
        return Matches(
            id = self.id,
            uuid = self.uuid,
            player1 = self.player1.id,
            player2 = self.player2.id,
            winner = self.winner.id,
            score = self.score,
        )
