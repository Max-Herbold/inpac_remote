import re

from flask import Blueprint, Flask, request

from .emailer import send
from .management.code_object import CodeObject
from .management.token_store import CredStore
from ..db_interface import user

app = Flask(__name__)
app.codes = {}
if not hasattr(app, "token_store"):
    app.token_store = CredStore()


def get_codes_dict() -> "dict[str, CodeObject]":
    """
    A dictionary of {email: CodeObject} pairs
    """
    return app.codes


def get_token_store() -> "CredStore":
    return app.token_store


request_code = Blueprint("request_code", __name__, url_prefix="/code")


ALLOWED_EXTENSIONS = {
    # TODO: Add more universities
    "rmit.edu.au",
    "student.rmit.edu.au",
    "student.monash.edu",
    "monash.edu",
}

email_re = re.compile(r"[^@]+@[^@]+\.[^@]+")


def _cleanup_codes():
    codes = get_codes_dict()
    for email, code in list(codes.items()):
        if code.is_expired():
            del codes[email]


@request_code.route("/new", methods=["POST"])
def new_code():
    # Removes expired codes
    _cleanup_codes()
    # grab the email from the request headers
    email = request.headers.get("email")

    if email is None:
        return {"response": "No email provided"}, 400

    codes = get_codes_dict()

    # rate limiting
    if email in codes and codes[email].time_since_creation < 30:
        return {"response": "Rate limiting"}, 400

    # don't allow 12 or more codes to exist
    if len(codes) >= 12:
        return {"response": "Rate limiting"}, 400

    # check if the email is valid
    if not email_re.match(email):
        return {"response": "Invalid email"}, 400

    if email.rsplit("@", 1)[1] not in ALLOWED_EXTENSIONS:
        return {"response": "Invalid email extension"}, 400

    # generate a code
    code_state = CodeObject()

    codes[email] = code_state

    body = f"Your code is {code_state.secret}\n\nThis code is valid for {code_state._live_for_seconds / 60:.0f} minutes."

    send([email], subject="2FA Code", body=body)

    return {"response": "Code sent"}, 200


@request_code.route("/verify", methods=["POST"])
def verify_code():
    _cleanup_codes()
    email = request.headers.get("email")
    code = request.headers.get("code")
    ip_header = request.headers.get("X-Real-IP", "Undetected")

    if email is None or code is None:
        return {"response": "No email or code provided"}, 400

    if email not in get_codes_dict():
        return {"response": "Code is not valid"}, 400

    code_state = get_codes_dict()[email]

    if code_state.validate_secret(code):
        user.user_login(email, ip_header)

        token = get_token_store().create_new_cred(email)
        return {"response": "Validated", "token": token}, 200
    else:
        return {"response": "Code is not valid"}, 400
