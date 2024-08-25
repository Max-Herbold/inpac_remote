import secrets
from dataclasses import dataclass

from .object import CredObject


@dataclass
class TokenObject(CredObject):
    email: str
    _live_for_seconds: float = 60 * 60  # 1 hour
    _length = 256
    _expire_on_valid = False

    def generate_secret(self):
        return secrets.token_urlsafe(self._length)

    def get_email(self):
        return self.email

    @property
    def _expected_length(self):
        if self._length % 3 == 0:
            return 4 * self._length // 3
        return 1 + 4 * self._length // 3
