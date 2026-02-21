from dataclasses import dataclass

from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchDTO():
    id : int = None
    uuid : str = None
    player1 : PlayerDTO = None
    player2 : PlayerDTO = None
    winner : int = None
    score : str = None