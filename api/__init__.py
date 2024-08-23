from flask import Blueprint

from .creds.request_code import request_code
from .creds.user import user_endpoint
from .test import test_bp

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def index():
    return "Flask API"


# Register all child blueprints here
api.register_blueprint(request_code)
api.register_blueprint(test_bp)
api.register_blueprint(user_endpoint)
