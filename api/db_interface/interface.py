import os

import mysql.connector
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
# go up two directories to find the .env file
BASEDIR = os.path.dirname(BASEDIR)
BASEDIR = os.path.dirname(BASEDIR)


class Database:
    conn: mysql.connector.MySQLConnection = None

    def connect() -> None:
        # Load the environment variables
        load_dotenv(os.path.join(BASEDIR, ".env"))

        host = os.getenv("db_host")
        user = os.getenv("db_user")
        password = os.getenv("db_password")
        database = os.getenv("db_database")

        Database.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

    def is_connected(self) -> bool:
        # conn might be None if it was never connected
        # it might still be defined if the connection was lost
        return Database.conn is not None and Database.conn.is_connected()

    def query(self, sql):
        try:
            cursor = Database.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, mysql.connector.errors.OperationalError):
            Database.connect()
            cursor = Database.conn.cursor()
            cursor.execute(sql)
        return cursor


# def Database.query(query, values=None):
#     mycursor = mydb.cursor(buffered=True)
#     mycursor.execute(query, values)
#     mydb.commit()
#     return mycursor


# print("Connected to database")
