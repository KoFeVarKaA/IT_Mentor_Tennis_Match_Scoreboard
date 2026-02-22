from sqlalchemy import select

from src.dto.dto_player import PlayerDTO
from src.dao.players.model import Players
from database import session_factory

class PlayersRepository():
    
    @staticmethod
    def get_by_id(player_id: int) -> Players:
        with session_factory() as session:
            player = session.get(Players, {"id": player_id})
            return player
        
    @staticmethod
    def get_by_name(player_name: int) -> Players:
        with session_factory() as session:
            player = session.query(Players).filter_by(name=player_name).first()
            return player
        
    @staticmethod
    def insert(dto : PlayerDTO) -> Players:
        player = dto.into_model()
        with session_factory() as session:
            session.add(player)
            session.commit()
            session.refresh(player)
        return player