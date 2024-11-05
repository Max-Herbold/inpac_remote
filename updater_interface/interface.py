import base64
import datetime
import json
import re
import threading
import time

import flask
from flask import Blueprint, request

from api.emailer import send, send_error

from .git_interact import get_all_data, update_remote, upload_data, PUBLIC_SECRET
from .support_functions import allowed_ip, get_parameter

HOST_IP_FIELD = "X-Real-IP"

update_interface = Blueprint(
    "update_interface", __name__, url_prefix="/update_interface"
)

last_updated_record = {}


@update_interface.route("/super_hidden_page_2843bccr2b8o7jhsagd8a7dg/")
def index():
    """
    It takes in a list of emails, a body, and a subject, and sends an email to each email in the list
    with the body and subject
    :return: status message, status_code
    """
    return_values = None

    args = dict(request.args)
    headers = dict(request.headers)
    ip = request.remote_addr  # This is an internal IP.
    client_ip = request.headers.get(HOST_IP_FIELD, ip)
    try:
        body_header = headers["Body"]
        body = base64.b64decode(body_header).decode("utf-8")  # Base64 decode the body
    except KeyError:
        body = "Body is empty."
    try:
        emails = args["emails"]
        emails = emails.split(",")
        if "" in emails:
            emails.remove("")
        if len(emails) == 0:
            send_error(
                "No destinations",
                body=f"There are no emails defined when reporting\r\n```\r\n{body}\r\n```",
            )
            return_values = "No emails provided", 401

        pattern = re.compile(r".{1,}@.{1,}\..{1,}")
        for j in emails:
            match = re.match(pattern, j)
            if match is None:
                error_info = f"Malformed email '{j}'"
                send_error(
                    "Invalid email",
                    body=f"There was an invalid email {j} in reporting\n```\n{body}\n```",
                )
                return error_info, 401
    except KeyError:
        emails = []
        # return "No emails provided", 401
    body += "\n\nThis is an automated message generated by the Python InPAC driver module.\n"
    if (len(emails) == 1 and emails[0].lower() == "max.herbold@rmit.edu.au") or len(
        emails
    ) == 0:
        body += f"origin IPv4: {client_ip}\n"
    try:
        subject = headers["Subject"]
    except KeyError:
        subject = ""
    try:
        send(emails, body, subject=subject)
        if return_values:
            # Some error had occurred but we still wanted to send the email
            return return_values
        return f"Email sent successfully to: {', '.join(emails)}", 200
    except Exception as e:
        send_error("INTERNAL ERROR", f"{e}")
        return "Failed, this has been logged", 500


@update_interface.route("/token")
def token():
    token = get_parameter("token", request)
    if token is None:
        return flask.abort(404)
    if token != PUBLIC_SECRET:
        return flask.abort(404)

    ip = request.remote_addr
    ip = request.headers.get(HOST_IP_FIELD, ip)

    id = get_parameter("id", request)
    version = get_parameter("version", request)
    version_to = get_parameter("version_to", request)
    allowed = allowed_ip(ip)

    # if the last update was more than 30 seconds ago, update the remote
    # prevent spamming
    if last_updated_record.get(id, 0) + 30 < time.time() or version_to is not None:
        # thread here
        t = threading.Thread(
            target=update_remote, args=(id, ip, version, version_to, allowed)
        )
        t.start()
    last_updated_record[id] = time.time()

    if not allowed:
        return "", 404
    return (
        "JjkGi/X0z4OECJtOX3Xi0kz86zQ4A+ZnQ4ougr8B4r6r5Pj/r8p0gw==,MSQlpMITfZdOZeobj7WpYA"
        + "==,yzNfyotfVjqvbF/0yOSXlA==,qSskOI8C6qRuo/PNOctgKw==",
        200,
    )


@update_interface.route("/ping")
def add_update_use():
    """
    Checks the request header token with PUBLIC_SECRET.
    If they match, record the IP and increment number of updates and version updating to.
    If they don't match, return an error.
    :return: status
    """
    data_points = ("version",)

    token = get_parameter("token", request)
    if token is None:
        return "No token provided", 401
    if token != PUBLIC_SECRET:
        return "Invalid token", 401

    # Record the data_points and increment number of updates.
    data = get_all_data()
    try:
        id = get_parameter("id", request)
        if id in data:
            for i in data_points:
                data[id][i] = get_parameter(i, request)
            data[id]["updates"] += 1
        else:
            data[id] = {i: get_parameter(i, request) for i in data_points}
            data[id]["updates"] = 1
        data[id]["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        upload_data(json.dumps(data, indent=2), id=id)

    except Exception as e:
        print(e)
        send_error("Error updating stats", f"{e}")
        return "Error updating stats", 500
    return "Successfully updated stats", 200
