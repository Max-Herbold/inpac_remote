from flask import Blueprint

from .code.request_code import request_code
from .test import test_bp

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def index():
    return "Flask API"


# Register all child blueprints here
api.register_blueprint(test_bp)
api.register_blueprint(request_code)
