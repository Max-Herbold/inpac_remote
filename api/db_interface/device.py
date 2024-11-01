from dataclasses import dataclass

from .device_log import get_device_logs, get_log_by_id, new_device_log
from .interface import Database


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

    last_action: str = None
    last_action_description: str = None
    last_action_timestamp: str = None

    def __post_init__(self):
        if self.last_log_id == -1:
            self.last_action = None
            self.last_action_description = None
            self.last_action_timestamp = None
            return

        last_log = get_log_by_id(self.last_log_id)
        self.last_action = last_log.action
        self.last_action_description = last_log.description
        self.last_action_timestamp = last_log.date

    def get_last_log(self):
        return get_log_by_id(self.id)

    def get_logs(self):
        return get_device_logs(self.id)


def create_new_device(
    created_by_id,
    model,
    serial_number,
    device_name,
    manufacturer,
    firmware_version,
    device_location,
    device_owner,
    device_action,
    additional_notes,
):
    """
    Creates a new device and returns the device object
    """
    query = (
        "INSERT INTO Device (model, serial_number, device_name, manufacturer, firmware_version, device_location, device_owner) "
        + "VALUES (%s, %s, %s, %s, %s, %s %s)"
    )
    Database.execute(
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

    return new_device_log(device_id, created_by_id, device_action, additional_notes)


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
