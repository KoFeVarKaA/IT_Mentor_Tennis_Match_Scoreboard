from src.controller.controller_main import MainController
from src.dao.matches.repository import MatchesRepository
from src.dao.players.repository import PlayersRepository
from src.service.service_mathes import MatchesService
from src.controller.controller_match_new import MatchNewController
from src.controller.controller_match_score import MatchScoreController
from src.controller.controller_matches import MatchesController
from src.view.render import Render


def controller_factory():
    return {
        "": MainController(),
        "new-match": MatchNewController(
            service=MatchesService(MatchesRepository, PlayersRepository), render=Render()),
        "match-score": MatchScoreController(
            service=MatchesService(MatchesRepository, PlayersRepository), render=Render()),
        "matches": MatchesController(
            service=MatchesService(MatchesRepository, PlayersRepository), render=Render()),   
    }