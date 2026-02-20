from src.dao.matches.repository import MatchesRepository
from src.dao.players.repository import PlayersRepository
from src.service.service_mathes import MatchesService
from src.controller.controller_match_new import MatchNewConroller
from src.controller.controller_match_score import MatchScoreController
from src.controller.controller_matches import MatchesController


def controller_factory():
    return {
        "new-match": MatchNewConroller(service=MatchesService(MatchesRepository, PlayersRepository)),
        "match-score": MatchScoreController(service=MatchesService(MatchesRepository, PlayersRepository)),
        "matches": MatchesController(service=MatchesService(MatchesRepository, PlayersRepository)),   
    }