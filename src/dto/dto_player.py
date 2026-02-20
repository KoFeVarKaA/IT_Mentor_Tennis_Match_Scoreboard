from dataclasses import dataclass


@dataclass(slots=True)
class PlayerDTO():
    id : int 
    name : str = None