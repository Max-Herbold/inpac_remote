import os

from dotenv import dotenv_values


def load_env() -> dict[str, str | None]:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # go up one directory to find the .env file
    BASEDIR = os.path.dirname(BASEDIR)

    return dotenv_values(os.path.join(BASEDIR, ".env"))
