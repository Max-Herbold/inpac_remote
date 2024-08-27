import os

import mysql.connector
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
print("path", os.path.join(BASEDIR, ".env"))

load_dotenv(os.path.join(BASEDIR, ".env"))
# assert load_dotenv(), "Failed to load .env file"

host = os.getenv("db_host")
user = os.getenv("db_user")
password = os.getenv("db_password")
database = os.getenv("db_database")


print(
    f"Connecting to database {host} as {user} with password {password} and database {database}"
)
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
)


def execute_query(query, values=None):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(query, values)
    mydb.commit()
    return mycursor


print("Connected to database")
