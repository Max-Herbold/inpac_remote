import os

from flask import Blueprint, Request, current_app, request, send_from_directory

js_loader = Blueprint("js_loader", __name__, url_prefix="/javascript")
css_loader = Blueprint("css_loader", __name__, url_prefix="/css")
asset_loader = Blueprint("asset_loader", __name__, static_folder="assets")


debug_mappings = {
    "secured_page.js": "debug_secured_page.js",
}


def _is_debugging() -> bool:
    return os.environ.get("DEBUG") == "True"


def _is_authenticated(r) -> bool:
    if r is None:
        return False
    token = r.cookies.get("token")
    return token is not None


def _is_debugging_and_not_authenticated(r: Request) -> bool:
    return _is_debugging() and not _is_authenticated(r)


def grab_file(filename: str, parent: str, r: Request = None) -> tuple[str, int]:
    if ".." in filename:
        return "Not Found", 404

    # if grabbing a debug file, make sure debug is enabled
    # debug files start with debug_
    if filename.startswith("debug_") and not (_is_debugging()):
        return "Not Found", 404

    if _is_debugging_and_not_authenticated(r):
        filename = debug_mappings.get(filename, filename)

    filename = filename.strip(".")
    root = os.path.dirname(__file__)
    return send_from_directory(f"{root}/{parent}", filename)


@js_loader.route("/<path:path>")
def js(path: str):
    if not path.endswith(".js"):
        return "Not Found", 404
    r = request
    return grab_file(path, parent="javascript", r=r)


@css_loader.route("/<path:path>")
def css(path: str):
    if not path.endswith(".css"):
        return "Not Found", 404
    return grab_file(path, parent="css")


def html(filename: str):
    if not filename.endswith(".html"):
        filename = f"{filename}.html"
    return grab_file(filename, parent="html")
