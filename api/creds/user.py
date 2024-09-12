import datetime
from dataclasses import dataclass

from flask import Blueprint, Flask, request

from ..db_interface.user import get_all_user_info, get_user_permission_level
from . import get_token_store

user_endpoint = Blueprint("user_endpoint", __name__, url_prefix="/user")


@dataclass
class User:
    email: str
    permission: int
    id: int
    ip_login: str
    last_login: datetime.datetime


@user_endpoint.route("/email", methods=["get"])
def get_email():
    token = request.cookies.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    email = _internal_get_email(token)

    if email is None:
        return {"response": "Invalid token"}, 400

    return {"response": "success", "email": email}


def _internal_get_email(token):
    token_store = get_token_store()
    email = token_store.get_email(token)
    return email


@user_endpoint.route("/validate", methods=["get"])
def validate():
    token = request.cookies.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    is_valid = _is_valid_token(token)

    return {"response": "success", "valid": is_valid}


def _get_all_user_info(email):
    return get_all_user_info(email)


def authenticate_user(fn=None, required_permission_level=0, user_email=None):
    """
    Decorator for @*.route() functions that require authentication.

    Usage:
    @*.route("/some_endpoint", methods=["GET"])
    @authenticate_user(required_permission_level=1)
    def some_endpoint():
        ...

    NOTE: This must be placed AFTER the route decorator otherwise will not be called
    when an endpoint is hit.

    Do not specify `fn`, this only allows `@authenticate_user()` or `@authenticate_user`.
    """

    def _authenticate_user(fn):
        """
        The `authenticate_user` function is a decorator that checks the validity of a token before allowing
        a user to access a specified function.

        Parameters
        ----------
        - fn: The `fn` parameter in the `authenticate_user` function is a function that will be passed as an
        argument to the `wrapper` function.

        Returns
        ----------
        - The `authenticate_user` function returns a wrapper function that checks the validity of a token
        before calling the original function `fn` with the provided arguments and keyword arguments. If the
        token is invalid, it returns a response indicating "Invalid token" with a status code of 403.
        """

        def __authenticate_user(*args, **kwargs):
            print(args, kwargs)
            token = request.cookies.get("token")

            is_valid = _is_valid_token(token)
            if not is_valid:
                return {"response": "No token provided"}, 401
            email = _internal_get_email(token)
            if email is None:
                return {"response": "Invalid token"}, 403
            if user_email is not None and email != user_email:
                return {"response": "Invalid user"}, 403

            if required_permission_level > 0:
                user_permission_level = get_user_permission_level(email)
                if user_permission_level is None:
                    return {"response": "Invalid user"}, 403
                if user_permission_level < required_permission_level:
                    return {"response": "Insufficient permissions"}, 403

            # check if the function accepts a user argument
            if fn.__code__.co_argcount == 1 and fn.__code__.co_varnames[0] == "user":
                user = _create_user_object(email)
                return fn(user)

            return fn()

        # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
        __authenticate_user.__name__ = fn.__name__

        return __authenticate_user

    if fn is None:
        # handles `@authenticate_user()`
        return _authenticate_user
    else:
        # handles `@authenticate_user`
        return _authenticate_user(fn)


def _is_valid_token(token):
    if token is None:
        return False
    token_store = get_token_store()
    return token_store.validate_token(token)


@user_endpoint.route("/logout", methods=["post"])
def logout():
    token = request.cookies.get("token")

    if token is None:
        return {"response": "No token provided"}, 401

    token_store = get_token_store()
    removed = token_store.remove_token(token)
    if not removed:
        return {"response": "Invalid token"}, 403

    return {"response": "success"}, 200


def _create_user_object(email):
    user = _get_all_user_info(email)

    return User(**user)
