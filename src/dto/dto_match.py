from dataclasses import dataclass, field

from src.dao.matches.model import Matches
from src.dto.dto_player import PlayerDTO


@dataclass(slots=True)
class MatchDTO():
    id : int = None
    uuid : str = None
    player1 : PlayerDTO = field(default_factory=PlayerDTO)
    player2 : PlayerDTO = field(default_factory=PlayerDTO)
    winner : PlayerDTO = field(default_factory=PlayerDTO)
    score : str = "0:0:0 0:0:0"
    score_dict : dict[str, int] = field(default_factory=lambda: {
            "player1_sets": 0,
            "player1_games": 0,
            "player1_points": 0,
            "player2_sets": 0,
            "player2_games": 0,
            "player2_points": 0,
        }) 
    add_point : int = None

    def to_dict(self):
        return {
            "id" : self.id ,
            "uuid" : self.uuid , 
            "player1" : self.player1 , 
            "player2" : self.player2 , 
            "winner" : self.winner , 
            "score" : self.score , 
            "score_dict": self.score_dict ,  
            "add_point": self.add_point ,
        }

    def into_model(self) -> Matches:
        return Matches(
            id = self.id,
            uuid = self.uuid,
            player1 = self.player1.id,
            player2 = self.player2.id,
            winner = self.winner.id,
            score = self.score,
        )

    def score_to_score_dict(self) -> None:
        score_split1, score_split2 = self.score.split(" ")
        score_split1 = score_split1.split(":")
        score_split2 = score_split2.split(":")
        self.score_dict = {
            "player1_sets" : score_split1[0],
            "player1_games" : score_split1[1],
            "player1_points" : score_split1[2],
            "player2_sets" : score_split2[0],
            "player2_games" : score_split2[1],
            "player2_points" : score_split2[2],
        }

    def score_dict_to_score(self) -> None:
        self.score = (
            f"{self.score_dict['player1_sets']}:{self.score_dict['player1_games']}:{self.score_dict['player1_points']} "
            f"{self.score_dict['player2_sets']}:{self.score_dict['player2_games']}:{self.score_dict['player2_points']}"
            )