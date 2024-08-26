from flask import Blueprint, Flask, request

from ..db_interface.user import get_user_permission_level
from . import get_token_store

user_endpoint = Blueprint("user_endpoint", __name__, url_prefix="/user")


@user_endpoint.route("/email", methods=["get"])
def get_email():
    token = request.headers.get("token")

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
    token = request.headers.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    is_valid = _is_valid_token(token)

    return {"response": "success", "valid": is_valid}


def authenticate_user(fn):
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

    def wrapper(required_permission_level=0, user_email=None):
        token = request.headers.get("token")

        is_valid = _is_valid_token(token)
        if not is_valid:
            return {"response": "Invalid token"}, 403
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

        return fn()

    return wrapper


def _is_valid_token(token):
    if token is None:
        return False
    token_store = get_token_store()
    return token_store.validate_token(token)


@user_endpoint.route("/logout", methods=["post"])
def logout():
    token = request.headers.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    token_store = get_token_store()
    token_store.remove_token(token)

    return {"response": "success"}
