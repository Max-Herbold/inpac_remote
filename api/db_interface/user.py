from dataclasses import dataclass

from .interface import Database


@dataclass
class User:
    id: int
    email: str
    ip_login: str
    last_login: str
    permission: int


def _new_user(email, ip, commit=True):
    query = "INSERT INTO User (email, ip_login, permission) VALUES (%s, %s, %s)"
    Database.execute(query, (email, ip, 0), commit=commit)


def user_login(email, ip):
    # check if the user exists
    query = "SELECT * FROM User WHERE email = %s"
    cursor = Database.query(query, (email,))
    result = cursor.fetchone()

    # if the user does not exist, create a new user
    if result is None:
        # since there is still another execute statement, we don't want to commit yet
        _new_user(email, ip, commit=False)
        cursor = Database.query(query, (email,))
        result = cursor.fetchone()

    # update the user's last login and ip
    query = "UPDATE User SET ip_login = %s, last_login=NOW() WHERE email=%s"
    Database.execute(query, (ip, email))


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


def get_all_user_info(email) -> dict:
    query = "SELECT * FROM User WHERE email = %s"
    cursor = Database.query(query, (email,))
    result = cursor.fetchone()

    if result is None:
        return None

    print(result)

    return {
        "id": result[0],
        "email": result[1],
        "ip_login": result[2],
        "last_login": result[3],
        "permission": result[4],
    }
