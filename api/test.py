from flask import Blueprint, request

test_bp = Blueprint("orbital", __name__)


@test_bp.route("/test")
def hello():
    return "Hello, World!"


@test_bp.route("/test2")
def hello2():
    return "Hello, World!2"
