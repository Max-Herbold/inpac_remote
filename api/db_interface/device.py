from dataclasses import dataclass

from .interface import Database
from .device_log import new_device_log


@dataclass
class Device:
    id: int
    model: str
    serial_number: str
    device_name: str  # alternative name
    manufacturer: str
    firmware_version: str
    device_location: str
    device_owner: str
    last_log_id: int = -1


def create_new_device(
    created_by_id,
    model,
    serial_number,
    device_name,
    manufacturer,
    firmware_version,
    device_location,
    device_owner,
):
    """
    Creates a new device and returns the device object
    """
    query = "INSERT INTO Device (model, serial_number, device_name, manufacturer, firmware_version, device_location, device_owner) VALUES (%s, %s, %s, %s, %s, %s %s)"
    Database.query(
        query,
        (
            model,
            serial_number,
            device_name,
            manufacturer,
            firmware_version,
            device_location,
            device_owner,
        ),
    )

    # also add a log for the device
    query = "SELECT LAST_INSERT_ID()"
    cursor = Database.query(query)
    device_id = cursor.fetchone()[0]

    return new_device_log(device_id, created_by_id, "create", "Device created")


def list_devices():
    """
    Returns a list of all devices
    """
    query = "SELECT * FROM Device"
    cursor = Database.query(query)
    devices = cursor.fetchall()

    listed = [Device(*device) for device in devices]
    # remove the first device
    return listed[1:]
