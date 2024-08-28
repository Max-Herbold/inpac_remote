from flask import Blueprint, request

test_bp = Blueprint("orbital", __name__)


@test_bp.route("/test")
def hello():
    return "Hello, World!"


@test_bp.route("/test2")
def hello2():
    return "Hello, World!2"


@test_bp.route("/test3")
def hello3():
    return "Hello, World!3"
