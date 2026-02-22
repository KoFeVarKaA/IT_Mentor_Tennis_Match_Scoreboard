from dataclasses import dataclass

from src.dao.matches.model import Matches
from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchDTO():
    id : int = None
    uuid : str = None
    player1 : PlayerDTO = PlayerDTO()
    player2 : PlayerDTO = PlayerDTO()
    winner : PlayerDTO = PlayerDTO()
    score : str = None

    def into_model(self) -> Matches:
        return Matches(
            id = self.id,
            uuid = self.uuid,
            player1 = self.player1.id,
            player2 = self.player2.id,
            winner = self.winner.id,
            score = self.score,
        )
