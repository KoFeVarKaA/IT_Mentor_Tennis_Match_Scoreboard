from sqlalchemy import func, or_, select
from sqlalchemy.orm import joinedload

from src.dao.players.model import Players
from src.dto.dto_match import MatchDTO
from src.dao.matches.model import Matches
from database import session_factory

class MatchesRepository():
    
    @staticmethod
    def get_by_id(match_id: int) -> Matches:
        with session_factory() as session:
            match = session.get(Matches, {"id": match_id})
            return match
        
    @staticmethod
    def get_all() -> list[Matches]:
        with session_factory() as session:
            query = select(Matches) 
            res = session.execute(query)
            matches = res.scalars().all()
            return matches
        
    @staticmethod
    def get_matches(
                offset: int = 0, 
                limit: int = 10, 
                player_name: str = None,
        ) -> list[Matches]:
        with session_factory() as session:
            query = (
                select(Matches)
                .join(
                    Players, or_(
                        Matches.player1 == Players.id,
                        Matches.player2 == Players.id,
                        Matches.winner == Players.id
                    ))
                .options(
                    joinedload(Matches.player1_obj),  
                    joinedload(Matches.player2_obj),  
                    joinedload(Matches.winner_obj),   
                )
                .offset(offset)
                .limit(limit)
            )
            if player_name:
                query = query.filter(Players.name.ilike(f"%{player_name}%"))

            matches = session.scalars(query).unique().all()
            return matches
        
    @staticmethod
    def get_matches_count(player_name: str = None) -> int:
        with session_factory() as session:
            query = select(func.count()).select_from(Matches).join(
                Players, or_(
                    Matches.player1 == Players.id,
                    Matches.player2 == Players.id,
                    Matches.winner == Players.id
                )
            )
            if player_name:
                query = query.filter(Players.name.ilike(f"%{player_name}%"))
            total_matches = session.scalars(query).first()
        return  total_matches
    
    @staticmethod
    def insert(dto : MatchDTO) -> Matches:
        match = dto.into_model()
        with session_factory() as session:
            session.add(match)
            session.commit()
            session.refresh(match)
        return match