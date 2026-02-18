from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Players(Base):
    """
    id —    первичный ключ, автоинкремент
    name —  имя игрока
    """

    __tablename__ = "players"


    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
