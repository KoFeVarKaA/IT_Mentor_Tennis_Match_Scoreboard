from jinja2 import Environment, FileSystemLoader, select_autoescape

from dto.dto_match import MatchDTO


class Render():
    def __init__(self):
        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html'])
            )
        self.match_score = env.get_template('match-score.html')
        self.matches = env.get_template('matches.html')

    

    def render_match_score(self, dto: MatchDTO):
        pass

    def render_matches(self, dto: MatchDTO):
        pass
    
