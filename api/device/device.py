from flask import Blueprint, Flask, request

from ..creds import authenticate_user

from ..db_interface.device import list_devices

device_bp = Blueprint("device", __name__, url_prefix="/device")


@device_bp.route("/list", methods=["get"])
# @authenticate_user
def list_devices_endpoint():
    devices = list_devices()
    return {"response": "success", "devices": devices}


# @device_bp.route("/add", methods=["post"])
