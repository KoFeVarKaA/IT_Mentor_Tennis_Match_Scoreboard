from dataclasses import dataclass

from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchDTO():
    id : int 
    uuid : str
    player1 : PlayerDTO
    player2 : PlayerDTO
    winner : int = None
    score : str = None