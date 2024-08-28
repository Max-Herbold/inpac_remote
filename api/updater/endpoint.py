import os

from flask import Blueprint, request

from ..env_loader import load_env

update_bp = Blueprint("update", __name__, url_prefix="/update")


def _update():
    # load env
    env_vars = load_env()
    print(env_vars)

    token = env_vars.get("GITHUB_TOKEN")

    # run git pull
    command = (
        f"git pull https://Max-Herbold:{token}@github.com/Max-Herbold/inpac_remote.git"
    )
    print("running pull", command)

    print(os.getcwd())

    # move to dir
    os.chdir("/home/inpac/inpac_remote")
    # git pull https://Max-Herbold:***@github.com/Max-Herbold/inpac_remote.git
    os.system(command)
    print("done")


# /api/update/update
@update_bp.route("/update")
def update():
    print("update hit")
    # run "/home/inpac/inpac_remote/updater.py"
    # subprocess.run([sys.executable, "/home/inpac/inpac_remote/updater.py"])
    _update()
    return {"response": "Update complete"}, 200
