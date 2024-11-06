import base64
import datetime
import json
import time

import requests

from api.env_loader import load_env

env_vars = load_env()

PUBLIC_SECRET = env_vars.get("GIT_PUBLIC_SECRET")
GITHUB_TOKEN = env_vars.get("GIT_GITHUB_TOKEN")
REPO = env_vars.get("GIT_REPO")
PATH = env_vars.get("GIT_PATH")

FIVE_MINUTES = 300
last_updated = time.time() - FIVE_MINUTES - 1
data: dict = None


def update_remote(id: str, ip: str, version: str, version_to: str, allowed: bool):
    """
    Updates the remote data.json file with the data from the request
    :param request: The request to get the data from
    :return: status
    """
    global data

    # Record the data_points and increment number of updates.
    new_data = {}
    new_data["ip"] = ip
    new_data["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data["version_to"] = version_to
    new_data["allowed_update"] = str(allowed)

    # update local data
    get_all_data()

    d_id: dict = data.get(id, None)

    if d_id is None:
        update_count = 0
    else:
        update_count = d_id.get("updates", 0)
    new_data["updates"] = update_count + (1 if version_to is None else 0)
    new_data["version"] = version or d_id.get("version", None)

    if id in data:
        data[id] |= new_data
    else:
        data[id] = new_data

    try:
        upload_data(json.dumps(data, indent=2), id)
        upload_data(json.dumps(data, indent=2), id, id)
    except Exception as e:
        print(e)


def get_all_data(file=PATH) -> dict:
    """
    Get the file from remote github repository
    """
    global data
    global last_updated

    if (time.time() - last_updated) < FIVE_MINUTES and data is not None:
        return data
    last_updated = time.time()

    header = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://raw.githubusercontent.com/{REPO}/main/{file}"
    r = requests.get(url, headers=header)
    unparsed = (
        r.text.replace("[", "").replace("]", "").replace("\\n", "").replace("\n", "")
    )
    data = json.loads(unparsed)
    return data


def upload_data(s: str, id: str = "pre 1.26.3", file=PATH) -> int:
    """
    Uploads a string to the server
    :param s: The string to upload
    :return: status code
    """
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO}/contents/{file}"
    attributes = requests.get(url, headers=headers)

    parsed_attributes: dict = json.loads(attributes.text)

    temp_data = {
        "message": f"update {id}",
        "content": base64.b64encode(str(s).encode("utf-8")).decode("utf-8"),
        "branch": "main",
    }
    if (sha := parsed_attributes.get("sha", None)) is not None:
        temp_data["sha"] = sha
    r = requests.put(
        f"https://api.github.com/repos/{REPO}/contents/{file}",
        headers=headers,
        json=temp_data,
    )
    return r.status_code
