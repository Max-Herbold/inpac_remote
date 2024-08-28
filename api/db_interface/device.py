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
    last_log_id: int = -1


def create_new_device(
    created_by_id,
    model,
    serial_number,
    device_name,
    manufacturer,
    firmware_version,
    device_location,
):
    """
    Creates a new device and returns the device object
    """
    query = "INSERT INTO Device (model, serial_number, device_name, manufacturer, firmware_version, device_location) VALUES (%s, %s, %s, %s, %s, %s)"
    Database.query(
        query,
        (
            model,
            serial_number,
            device_name,
            manufacturer,
            firmware_version,
            device_location,
        ),
    )

    # also add a log for the device
    query = "SELECT LAST_INSERT_ID()"
    cursor = Database.query(query)
    device_id = cursor.fetchone()[0]

    new_device_log(device_id, created_by_id, "create", "Device created")


# create_new_device(
#     1,
#     "model",
#     "serial_number",
#     "device_name",
#     "manufacturer",
#     "firmware_version",
#     "device_location",
# )
