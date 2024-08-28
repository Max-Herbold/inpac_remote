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

    r = _update()
    if r != 0:
        return {"response": "Update failed"}, 500
    return {"response": "Update complete"}, 200
