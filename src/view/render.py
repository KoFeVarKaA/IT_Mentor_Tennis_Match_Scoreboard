from jinja2 import Environment, FileSystemLoader, select_autoescape


class Render():
    def __init__(self):
        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html'])
            )
        self.new_match = env.get_template('new-match.html')
        self.match_score = env.get_template('match-score.html')
        self.matches = env.get_template('matches.html')

    

    def render_new_match(self, dto):
        pass

    def render_match_score(self, dto):
        pass

    def render_matches(self, dto):
        pass
    
