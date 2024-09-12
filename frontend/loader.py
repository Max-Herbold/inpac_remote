import os

from flask import Blueprint, Request, current_app, request, send_from_directory

js_loader = Blueprint("js_loader", __name__, url_prefix="/javascript")
css_loader = Blueprint("css_loader", __name__, url_prefix="/css")
asset_loader = Blueprint("asset_loader", __name__, static_folder="assets")


def grab_file(filename: str, parent: str):
    if ".." in filename:
        return "Not Found", 404

    if "debug_login" in filename and not (os.environ.get("DEBUG") == "True"):
        return "Not Found", 404

    filename = filename.strip(".")
    root = os.path.dirname(__file__)
    return send_from_directory(f"{root}/{parent}", filename)


@js_loader.route("/<path:path>")
def js(path: str):
    if not path.endswith(".js"):
        return "Not Found", 404
    return grab_file(path, parent="javascript")


@css_loader.route("/<path:path>")
def css(path: str):
    if not path.endswith(".css"):
        return "Not Found", 404
    return grab_file(path, parent="css")


def html(filename: str):
    if not filename.endswith(".html"):
        # return "Not Found", 404
        filename = f"{filename}.html"
    return grab_file(filename, parent="html")
