import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from src.dao.matches.repository import MatchesRepository
from src.dao.players.repository import PlayersRepository
from src.dto.dto_match import MatchDTO
from src.dto.dto_player import PlayerDTO
from src.service.service_mathes import MatchesService

class TestMatchesService(unittest.TestCase):
    def setUp(self):
        self.service = MatchesService(MatchesRepository, PlayersRepository)

    def test_40_40_points_way(self):
        """Если игрок 1 выигрывает очко при счёте 40-40, гейм не заканчивается"""
        dto = MatchDTO(
            player1=PlayerDTO(id=1, name="Player 1"),
            player2=PlayerDTO(id=2, name="Player 2"),
            score_dict={
                "player1_sets": 0,
                "player1_games": 0,
                "player1_points": "30",
                "player2_sets": 0,
                "player2_games": 0,
                "player2_points": "40",
            },
            add_point=1,
        )

        dto = self.service._render_score(dto)

        self.assertEqual(dto.score_dict["player1_points"], "Равно")
        self.assertEqual(dto.score_dict["player2_points"], "Равно")

    def test_40_0_points_way(self):
        """Если игрок 1 выигрывает очко при счёте 40-0, то он выигрывает и гейм"""
        dto = MatchDTO(
            player1=PlayerDTO(id=1, name="Player 1"),
            player2=PlayerDTO(id=2, name="Player 2"),
            score_dict={
                "player1_sets": 0,
                "player1_games": 0,
                "player1_points": "40",
                "player2_sets": 0,
                "player2_games": 0,
                "player2_points": "0",
            },
            add_point=1,
        )

        dto = self.service._render_score(dto)

        self.assertEqual(dto.score_dict["player1_points"], "0")
        self.assertEqual(dto.score_dict["player2_points"], "0")


    def test_6_6_games_way(self):
        """При счёте 6-6 начинается тайбрейк вместо обычного гейма"""
        dto = MatchDTO(
            player1=PlayerDTO(id=1, name="Player 1"),
            player2=PlayerDTO(id=2, name="Player 2"),
            score_dict={
                "player1_sets": 0,
                "player1_games": 5,
                "player1_points": "40",
                "player2_sets": 0,
                "player2_games": 6,
                "player2_points": "0",
            },
            add_point=1,
        )

        dto = self.service._render_score(dto)

        self.assertEqual(dto.score_dict["player1_points"], "Тай-брейк,0")
        self.assertEqual(dto.score_dict["player2_points"], "Тай-брейк,0")
        self.assertEqual(dto.winner.id, None)
    

if __name__ == "__main__":
    unittest.main()