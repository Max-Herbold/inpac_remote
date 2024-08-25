import secrets
from dataclasses import dataclass

from .object import CredObject


@dataclass
class CodeObject(CredObject):
    _live_for_seconds: float = 120
    _length: int = 8
    _expire_on_valid = True

    def generate_secret(self) -> str:
        # create a random 6 digit integer code
        number = secrets.randbelow(10 ** (self._length))
        return f"{number:0{self._length}}"
