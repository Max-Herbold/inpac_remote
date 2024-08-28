from dataclasses import dataclass

from .interface import Database


@dataclass
class User:
    id: int
    email: str
    ip_login: str
    last_login: str
    permission: int


def _new_user(email, ip):
    query = "INSERT INTO User (email, ip_login, permission) VALUES (%s, %s, %s)"
    Database.query(query, (email, ip, 0))


def user_login(email, ip):
    # check if the user exists
    query = "SELECT * FROM User WHERE email = %s"
    cursor = Database.query(query, (email,))
    result = cursor.fetchone()

    # if the user does not exist, create a new user
    if result is None:
        _new_user(email, ip)
        cursor = Database.query(query, (email,))
        result = cursor.fetchone()

    # update the user's last login and ip
    query = "UPDATE User SET ip_login = %s, last_login = NOW() WHERE email = %s"
    Database.query(query, (ip, email))


def get_user_permission_level(email) -> int:
    """
    0 - indicates no special permissions
    1 - authorized to view all devices
    2 - authorized to add and remove devices
    3 - admin
    """
    query = "SELECT permission FROM User WHERE email = %s"
    cursor = Database.query(query, (email,))
    result = cursor.fetchone()

    if result is None:
        return None

    return result[0]
