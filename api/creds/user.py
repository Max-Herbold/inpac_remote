from flask import Blueprint, Flask, request

from . import get_token_store

user_endpoint = Blueprint("user_endpoint", __name__, url_prefix="/user")


@user_endpoint.route("/email", methods=["get"])
def get_email():
    token = request.headers.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    token_store = get_token_store()
    print(token_store, token)
    email = token_store.get_email(token)

    if email is None:
        return {"response": "Invalid token"}, 400

    return {"response": "success", "email": email}


@user_endpoint.route("/validate", methods=["get"])
def validate():
    token = request.headers.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    token_store = get_token_store()
    valid = token_store.validate_token(token)

    return {"response": "success", "valid": valid}


@user_endpoint.route("/logout", methods=["post"])
def logout():
    token = request.headers.get("token")

    if token is None:
        return {"response": "No token provided"}, 400

    token_store = get_token_store()
    token_store.remove_token(token)

    return {"response": "success"}
