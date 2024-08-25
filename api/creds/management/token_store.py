import typing

from .token_object import TokenObject


class CredStore:
    def __init__(self):
        self._creds: typing.Dict[str, TokenObject] = {}

    def _remove_cred_by_secret(self, secret: str):
        try:
            del self._creds[secret]
        except KeyError:
            pass  # ignore if the secret doesn't exist

    def _remove_cred_by_email(self, email: str):
        items = list(self._creds.items())
        for secret, cred in items:
            if cred.get_email() == email:
                self._remove_cred_by_secret(secret)

    def _add_cred(self, cred: "TokenObject"):
        # remove any existing creds with the same email
        self._remove_cred_by_email(cred.get_email())

        self._creds[cred.secret] = cred

    def _get_cred(self, token: str) -> "TokenObject":
        return self._creds.get(token, None)

    def get_email(self, token: str) -> str:
        cred = self._get_cred(token)
        if self._validate_token(token, cred):
            return cred.get_email()
        return None

    def _validate_token(self, token: str, cred: "TokenObject | None") -> bool:
        if cred is None:
            return False
        return cred.validate_secret(token)

    def remove_token(self, token: str):
        self._remove_cred_by_secret(token)

    def validate_token(self, token: str) -> bool:
        cred = self._get_cred(token)
        return self._validate_token(token, cred)

    def create_new_cred(self, email: str):
        """
        The function creates a new credential object with a given email and returns the secret
        associated with it.

        Parameters
        ----------
        - email (str): The `create_new_cred` method takes an email address as a parameter. It creates a
        new `TokenObject` instance with the provided email address, adds it to the credentials list, and
        then returns the secret associated with that credential.

        Returns
        ----------
        - The code snippet is returning the secret attribute of the cred object that is created.
        """
        cred = TokenObject(email)
        self._add_cred(cred)
        return cred.secret
