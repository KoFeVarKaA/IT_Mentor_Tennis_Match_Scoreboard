from dataclasses import dataclass

from src.dao.players.model import Players


@dataclass(slots=True)
class PlayerDTO():
    id : int = None
    name : str = None

    def into_model(self) -> Players:
        return Players(
            id = self.id, 
            name = self.name,
        )