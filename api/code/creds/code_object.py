import secrets
from dataclasses import dataclass

from .object import CredObject


@dataclass
class CodeObject(CredObject):
    _live_for_seconds: float = 120
    length: int = 6

    def generate_secret(self) -> str:
        # create a random 6 digit integer code
        number = secrets.randbelow(10 ** (self.length + 1))
        return f"{number:06}"
