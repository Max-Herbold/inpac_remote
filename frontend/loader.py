from flask import Blueprint, Request, current_app, request, send_file
import os

js_loader = Blueprint("js_loader", __name__, url_prefix="/javascript")
css_loader = Blueprint("css_loader", __name__, url_prefix="/css")


def grab_file(filename: str, parent: str):
    if ".." in filename:
        return "Not Found", 404
    filename = filename.strip(".")
    root = os.path.dirname(__file__)
    full_path = f"{root}/{parent}/{filename}"
    if not os.path.exists(full_path):
        return "Not Found", 404
    if os.path.isdir(full_path):
        return "Not Found", 404
    # if the file is not in the root directory, return 404
    for root, dirs, files in os.walk(root):
        if filename in files:
            break
    else:
        return "Not Found", 404
    return send_file(f"{root}/{filename}")


@js_loader.route("/<filename>")
def js(filename: str):
    if not filename.endswith(".js"):
        return "Not Found", 404
    return grab_file(filename, parent="javascript")


@css_loader.route("/<filename>")
def css(filename: str):
    if not filename.endswith(".css"):
        return "Not Found", 404
    return grab_file(filename, parent="css")


def html(filename: str):
    if not filename.endswith(".html"):
        return "Not Found", 404
    return grab_file(filename, parent="html")
