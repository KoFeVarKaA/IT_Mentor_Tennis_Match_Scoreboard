from sqlalchemy import select
from src.dto.dto_match import MatchDTO
from src.dao.matches.model import Matches
from database import session_factory

class MatchesRepository():
    
    @staticmethod
    def get_by_id(match_id: int) -> Matches:
        with session_factory() as session:
            order = session.get(Matches, {"id": match_id})
            return order
        
    @staticmethod
    def get_all() -> list[Matches]:
        with session_factory() as session:
            query = select(Matches) 
            res = session.execute(query)
            orders = res.scalars().all()
            return orders
        
    @staticmethod
    def insert(dto : MatchDTO) -> Matches:
        match = dto.into_model()
        with session_factory() as session:
            session.add(match)
            session.commit()
            session.refresh(match)
        return match