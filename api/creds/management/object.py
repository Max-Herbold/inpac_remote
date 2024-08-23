import time


class CredObject:
    def __post_init__(self):
        self._secret: str = self.generate_secret()
        self._time = time.time()
        self._attempts = 0
        self._max_attempts = 3

    @property
    def secret(self):
        return self._secret

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

    def generate_secret() -> str:
        raise NotImplementedError("Monkeypatch this.")

    def _increment_attempts(self):
        self._attempts += 1
        if self._attempts > self._max_attempts:
            self._time = 0  # expire the code

    def validate_secret(self, secret: str):
        if self.is_expired():
            return False

        assert isinstance(secret, str)
        assert isinstance(self._secret, str)

        assert len(self._secret) == self._expected_length

        valid = self._secret == secret
        if not valid:
            self._increment_attempts()
        return valid

    @property
    def _expected_length(self):
        return self._length
