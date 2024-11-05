import os
import typing

import mysql.connector

import functools

if typing.TYPE_CHECKING:
    from mysql.connector.cursor import MySQLCursor


BASEDIR = os.path.abspath(os.path.dirname(__file__))
# go up two directories to find the .env file
BASEDIR = os.path.dirname(BASEDIR)
BASEDIR = os.path.dirname(BASEDIR)


@functools.lru_cache()
def grab_env_vars() -> dict:
    # If running in GitHub Actions, use os.getenv directly
    if os.getenv("GITHUB_ACTIONS") == "true":
        env_vars = {
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            "DB_DATABASE": os.getenv("DB_DATABASE"),
        }
    else:
        # Local environment, use load_env()
        from ..env_loader import load_env

        env_vars = load_env() or {}

    # Ensure sensitive data (e.g., passwords) is handled safely
    for k, v in env_vars.items():
        if k == "DB_PASSWORD":
            print(f"{k}: [REDACTED]")
        else:
            print(f"{k}: {v}")
    return env_vars


class Database:
    conn: mysql.connector.MySQLConnection = None

    def __init__(self):
        if not self.is_connected():
            Database.connect()

    def connect() -> None:
        # Load the environment variables
        env_vars: dict = grab_env_vars()

        host = env_vars.get("DB_HOST")
        user = env_vars.get("DB_USER")
        password = env_vars.get("DB_PASSWORD")
        database = env_vars.get("DB_DATABASE")

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
    def execute(sql, values=None, commit=True) -> "MySQLCursor":
        cursor = Database._query(sql, values)
        if commit:
            Database.commit()
        return cursor

    @staticmethod
    def commit():
        Database.conn.commit()

    @staticmethod
    def close():
        Database.conn.close()
