import os

from dotenv import load_dotenv


def load_env():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # go up one directory to find the .env file
    BASEDIR = os.path.dirname(BASEDIR)
    print("env_loader.py: root", os.path.join(BASEDIR, ".env"))

    res = load_dotenv(os.path.join(BASEDIR, ".env"))
    print("env_loader.py: loaded env", res)
    return res
