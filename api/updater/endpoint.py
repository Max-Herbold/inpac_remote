from flask import Blueprint, request
import sys
import subprocess

update_bp = Blueprint("update", __name__, url_prefix="/update")


# /api/update/update
@update_bp.route("/update")
def update():
    print("update hit")
    # run "/home/inpac/inpac_remote/updater.py"
    subprocess.run([sys.executable, "/home/inpac/inpac_remote/updater.py"])
    return "Update complete", 200
