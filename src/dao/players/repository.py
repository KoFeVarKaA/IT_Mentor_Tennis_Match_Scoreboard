from sqlalchemy import select
from src.dao.players.model import Players
from database import session_factory

class PlayersRepository():
    
    @staticmethod
    def get_by_id(match_id: int) -> Players:
        with session_factory() as session:
            order = session.get(Players, {"id": match_id})
            return order