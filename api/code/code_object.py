import secrets
import time
from dataclasses import dataclass


@dataclass
class CodeObject:
    def __post_init__(self):
        self._time = time.time()
        self._code = CodeObject.generate_code()

        self._live_for_seconds: float = 120

    @staticmethod
    def generate_code():
        # create a random 6 digit integer code
        number = secrets.randbelow(1000000)
        return f"{number:06}"

    @property
    def code(self):
        return self._code

    @property
    def time(self):
        return self._time

    @property
    def time_since_creation(self):
        return time.time() - self._time

    def is_expired(self):
        return self.time_since_creation > self._live_for_seconds

    def is_active(self):
        return not self.is_expired()

    def __repr__(self):
        return f"CodeObject(code={self._code[:-5]}nnnnn, time={self._time})"
