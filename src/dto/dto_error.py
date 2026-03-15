from dataclasses import dataclass

@dataclass(slots=True)
class ErrorDTO():
    status_code: int
    message: str = ""