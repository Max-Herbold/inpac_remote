import re

from .creds.code_object import CodeObject

from flask import Blueprint, Flask, request, send_from_directory

from .emailer import send

app = Flask(__name__)
app.codes = {}


def get_codes_dict() -> "dict[str, CodeObject]":
    return app.codes


request_code = Blueprint("request_code", __name__, url_prefix="/requestCode")

email_re = re.compile(r"[^@]+@[^@]+\.[^@]+")


@request_code.route("/code", methods=["POST"])
def code():
    # grab the email from the request headers
    email = request.headers.get("email")

    if email is None:
        return {"response": "No email provided"}, 400

    # check if the email is valid
    if not email_re.match(email):
        return {"response": "Invalid email"}, 400

    # TODO: check time
    #

    # generate a code
    code_state = CodeObject()
    codes = get_codes_dict()
    codes[email] = code_state

    print(email, code)
    print(get_codes_dict())

    send([email], subject="2FA Code", body=f"Your code is {code_state.code}")

    return {"response": "Code sent"}, 200
