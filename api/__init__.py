from flask import Blueprint
from .test import test_bp

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def index():
    return "Flask API"


# Register all child blueprints here
api.register_blueprint(test_bp)
