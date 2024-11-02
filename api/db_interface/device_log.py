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
    query = "INSERT INTO Device_Log (device_id, user_id, date, action, description) VALUES (%s, %s, NOW(), %s, %s)"
    Database.execute(query, (device_id, created_by_id, action, description))

    # go back and update the device object with the last log id
    query = "SELECT LAST_INSERT_ID()"
    cursor = Database.query(query)
    last_log_id = cursor.fetchone()[0]

    query = "UPDATE Device SET last_log_id = %s WHERE id = %s"
    Database.query(query, (last_log_id, device_id))

    return {"response": "success"}


def get_device_logs(device_id):
    query = "SELECT * FROM Device_Log WHERE device_id = %s"
    cursor = Database.query(query, (device_id,))
    logs = cursor.fetchall()

    return [DeviceLog(*log) for log in logs]


def get_last_device_log(device_id):
    query = "SELECT * FROM Device_Log WHERE device_id = %s ORDER BY date DESC LIMIT 1"
    cursor = Database.query(query, (device_id,))
    log = cursor.fetchone()

    return DeviceLog(*log)


def get_log_by_id(log_id):
    query = "SELECT * FROM Device_Log WHERE id = %s"
    cursor = Database.query(query, (log_id,))
    log = cursor.fetchone()

    return DeviceLog(*log)
