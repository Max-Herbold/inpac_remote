import os
import typing

import mysql.connector

if typing.TYPE_CHECKING:
    from mysql.connector.cursor import MySQLCursor

from ..env_loader import load_env

BASEDIR = os.path.abspath(os.path.dirname(__file__))
# go up two directories to find the .env file
BASEDIR = os.path.dirname(BASEDIR)
BASEDIR = os.path.dirname(BASEDIR)


class Database:
    conn: mysql.connector.MySQLConnection = None

    def __init__(self):
        if not self.is_connected():
            Database.connect()

    def connect() -> None:
        # Load the environment variables
        env_vars: dict = load_env()

        host = env_vars.get("db_host")
        user = env_vars.get("db_user")
        password = env_vars.get("db_password")
        database = env_vars.get("db_database")

        Database.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

    def __del__(self):
        if self.is_connected():
            Database.close()

    def is_connected(self) -> bool:
        # conn might be None if it was never connected
        # it might still be defined if the connection was lost
        return Database.conn is not None and Database.conn.is_connected()

    @staticmethod
    def _query(sql, values=None):
        try:
            cursor = Database.conn.cursor()
            cursor.execute(sql, values)
        except (AttributeError, mysql.connector.errors.OperationalError):
            Database.connect()
            cursor = Database.conn.cursor()
            cursor.execute(sql, values)
        return cursor

    @staticmethod
    def query(sql, values=None) -> "MySQLCursor":
        return Database._query(sql, values)

    @staticmethod
    def execute(sql, values=None) -> "MySQLCursor":
        cursor = Database._query(sql, values)
        Database.commit()
        return cursor

    @staticmethod
    def commit():
        Database.conn.commit()

    @staticmethod
    def close():
        Database.conn.close()
