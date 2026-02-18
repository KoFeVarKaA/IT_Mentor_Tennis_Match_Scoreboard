from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Matches(Base):
    """
    id —            первичный ключ, автоинкремент
    uuid —          уникальный идентификатор матча
    player1_id —    идентификатор первого игрока, внешний ключ на players.id
    player2_id —    идентификатор второго игрока, внешний ключ на players.id
    winner_id —     идентификатор победителя,     внешний ключ на players.id
    score —         JSON-представление счёта матча
    """

    __tablename__ = "matches"


    id : Mapped[int] = mapped_column(primary_key=True)
    uuid : Mapped[str]
    player1 : Mapped[int] = mapped_column(ForeignKey('players.id'))
    player2 : Mapped[int] = mapped_column(ForeignKey('players.id'))
    winner : Mapped[int] = mapped_column(ForeignKey('players.id'))
    score : Mapped[str]