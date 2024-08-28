import os
from typing import Dict

from dotenv import dotenv_values


def load_env() -> dict[str, str | None]:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # go up one directory to find the .env file
    BASEDIR = os.path.dirname(BASEDIR)
    print("env_loader.py: root", os.path.join(BASEDIR, ".env"))

    res = dotenv_values(os.path.join(BASEDIR, ".env"))
    print("env_loader.py: loaded env", res)
    return res
