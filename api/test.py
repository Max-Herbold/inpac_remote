from flask import Blueprint, request

test_bp = Blueprint("orbital", __name__)


@test_bp.route("/test")
def hello():
    return {"response": "success"}, 200
