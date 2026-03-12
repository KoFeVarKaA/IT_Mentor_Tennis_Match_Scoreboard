from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.dto.dto_matches import MatchesDTO
from src.dto.dto_match import MatchDTO


class Render():
    def __init__(self):
        env = Environment(
            loader=FileSystemLoader('src/view/templates'),
            autoescape=select_autoescape(['html'])
            )
        self.match_score = env.get_template('match-score.html')
        self.matches = env.get_template('matches.html')
        self.winner = env.get_template('winner.html')

        env_error = Environment(
            loader=FileSystemLoader('src/view/errors'),
            autoescape=select_autoescape(['html'])
            )
        self.input_error = env_error.get_template('input_error.html')

    def render_winner(self, dto: MatchDTO):
        return self.winner.render(dto=dto.to_dict()).encode('utf-8')

    def render_match_score(self, dto: MatchDTO):
        return self.match_score.render(dto=dto.to_dict()).encode('utf-8')

    def render_matches(self, dto: MatchesDTO):
        return self.matches.render(dto=dto.to_dict()).encode('utf-8')

    def render_input_error(self, variables: dict):
        return self.input_error.render(variables=variables).encode('utf-8')
