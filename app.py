from dotenv import load_dotenv
from flask import Flask

from api import api
from frontend.loader import asset_loader, css_loader, html, js_loader

app = Flask(__name__)
app.sockets = []

# Register backend
app.register_blueprint(api)


# Register frontend
app.register_blueprint(css_loader)
app.register_blueprint(js_loader)
app.register_blueprint(asset_loader)


@app.route("/")
@app.route("/<path>")
@app.route("/<path>.html")
def hello_world(path=None):
    """
    The `hello_world` function returns the HTML content of a specified path or defaults to "index.html".

    Parameters
    ----------
    - path: The `path` parameter in the `hello_world` function is a string that represents the file path
    of the HTML file to be returned. If no `path` is provided when calling the function, it defaults to
    "index".

    Returns
    ----------
    - The function `hello_world` is returning the HTML content of the file specified by the `path`
    parameter. If `path` is not provided, it defaults to "index.html".
    """
    if path is None:
        path = "index"
    return html(f"{path}")


if __name__ == "__main__":
    app.run(ssl_context=("cert.pem", "key.pem"), port=443)
