from dataclasses import dataclass

from .interface import Database


@dataclass
class DeviceLog:
    id: int
    device_id: int
    user_id: int
    date: str
    action: str
    description: str


def new_device_log(device_id, created_by_id, action: str, description: str):
    query = "INSERT INTO device_log (device_id, user_id, date, action, description) VALUES (%s, %s, NOW(), %s, %s)"
    Database.query(query, (device_id, created_by_id, action, description))

    # go back and update the device object with the last log id
    query = "SELECT LAST_INSERT_ID()"
    cursor = Database.query(query)
    last_log_id = cursor.fetchone()[0]

    query = "UPDATE device SET last_log_id = %s WHERE id = %s"
    Database.query(query, (last_log_id, device_id))
