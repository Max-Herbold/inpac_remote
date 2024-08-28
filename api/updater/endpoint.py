import hashlib
import os

import requests
from flask import Blueprint, abort, request

from ..env_loader import load_env

update_bp = Blueprint("update", __name__, url_prefix="/update")


def _update():
    # load env
    env_vars = load_env()

    token = env_vars.get("GH_TOKEN")

    # run git pull
    command = (
        f"git pull https://Max-Herbold:{token}@github.com/Max-Herbold/inpac_remote.git"
    )

    # move to dir
    os.chdir("/home/inpac/inpac_remote")
    # git pull https://Max-Herbold:***@github.com/Max-Herbold/inpac_remote.git
    return os.system(command)


# /api/update/update
@update_bp.route("/update")
def update():
    # run "/home/inpac/inpac_remote/updater.py"
    # subprocess.run([sys.executable, "/home/inpac/inpac_remote/updater.py"])

    auth_token = request.headers.get("Update-Token")
    if auth_token is None:
        abort(401)

    # check if the token is correct
    if (
        hashlib.md5(auth_token.encode()).hexdigest()
        != "c6a8b4cd30e8896571151409c7843739"
    ):
        abort(403)

    try:
        r = _update()
        if r != 0:
            return {"response": "Update failed (2)"}, 500
    except Exception:
        return {"response": "Update failed (1)"}, 500

    return {"response": "Update complete"}, 200
