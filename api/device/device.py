import typing

from flask import Blueprint, Flask, request

from ..creds import authenticate_user
from ..db_interface.device import create_new_device, list_devices

if typing.TYPE_CHECKING:
    from ..creds.user import User


device_bp = Blueprint("device", __name__, url_prefix="/device")


@device_bp.route("/list", methods=["get"])
@authenticate_user()
def list_devices_endpoint():
    devices = list_devices()
    return {"response": "success", "devices": devices}


@device_bp.route("/add", methods=["post"])
@authenticate_user(required_permission_level=0)
def add_device(user: "User"):
    data: dict = request.json
    print(request)
    print(request.json)
    # print(request.json)
    print(user)

    user_id = user.id
    device_location = data.get("device_location")
    device_owner = data.get("device_owner")
    device_action = data.get("device_action")
    model = data.get("device_model")
    manufacturer = data.get("device_manufacturer")
    serial_number = data.get("device_serial_number")  # optional
    device_name = data.get("device_name")  # optional
    firmware_version = data.get("firmware_version")  # optional
    additional_notes = data.get("additional_notes")  # optional

    if model is None:
        return {"response": "error", "error": "Model is required"}, 400
    if manufacturer is None:
        return {"response": "error", "error": "Manufacturer is required"}, 400
    if device_location is None:
        return {"response": "error", "error": "Device location is required"}, 400
    if device_action == "create" and device_owner is None:
        return {
            "response": "error",
            "error": "Device owner is required when creating a device",
        }, 400

    try:
        response = create_new_device(
            user_id,
            model,
            serial_number,
            device_owner,
            device_name,
            manufacturer,
            firmware_version,
            device_location,
            device_action,
            additional_notes,
        )

        return response, 200
    except Exception as e:
        return {"response": "error", "error": str(e)}, 400
