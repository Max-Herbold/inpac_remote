import secrets
from dataclasses import dataclass

from .object import CredObject


@dataclass
class TokenObject(CredObject):
    _live_for_seconds: float = 60 * 60  # 1 hour
    length = 256

    def generate_secret(self):
        return secrets.token_urlsafe(self.length)
