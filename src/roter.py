from src.controller.controller_match_new import MatchNewConroller
from src.controller.controller_match_score import MatchScoreController
from src.controller.controller_matches import MatchesController


def controller_factory(database):
    return {
        "new-match": MatchNewConroller,
        "match-score": MatchScoreController,
        "matches": MatchesController,   
    }