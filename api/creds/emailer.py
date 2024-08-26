import smtplib
from ipaddress import ip_address, ip_network

from flask import Flask, request, send_from_directory

from ._emailer_creds import gmail_password, gmail_user

app = Flask(__name__)
current_codes: dict = None

THIRTY_SECONDS = 30

ignored_cidr = ()  # example: "192.168.0.0/24",

last_updated_record = {}


def allowed_ip(ip: str) -> bool:
    """
    Checks if an IP is in the ignored_cidr list
    :param ip: The IP to check e.g. 192.168.0.1
    :return: True if the IP is in the ignored_cidr list, False otherwise
    """
    for i in ignored_cidr:
        if ip_address(ip) in ip_network(i):
            return False
    return True


def send(to: list, body=None, cc=None, bcc=None, subject="ALERT"):
    """
    It sends an email to the list of recipients (to) with the given subject and body

    :param to: list of email addresses to send to
    :type to: list
    :param body: The body of the email
    :param cc: Carbon copy. This is a list of email addresses that will receive a copy of the email
    :param bcc: Blind carbon copy. This is a list of email addresses that will receive the email, but
    will not be visible to the other recipients
    :param subject: The subject of the email, defaults to ALERT (optional)
    """
    if to is None:
        to = ["max.herbold@rmit.edu.au"]
        subject = "NO REP - " + subject
    if body is None:
        body = ""
    if cc is None:
        cc = []
    if bcc is None:
        bcc = []
    bcc.append("maxher349@gmail.com")

    sent_from = f"InPAC ALERT <{gmail_user}>"

    message = (
        "From: %s\r\n" % sent_from
        + "To: %s\r\n" % ",".join(to)
        + "CC: %s\r\n" % ",".join(cc)
        + "Subject: %s\r\n" % subject
        + "\r\n"
        + body
        + "\r\n"
    )

    recipients = to + cc + bcc

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, recipients, message)
        server.close()

        print("Email sent!")
    except Exception as e:
        print("Something went wrong...")
        print(e)


def send_error(subject: str, body: str = " "):
    to = ["max.herbold@rmit.edu.au"]
    subject = "SEND ERROR - " + subject

    send(to=to, body=body, subject=subject)


def get_parameter(name, req):
    """
    Gets a parameter from the request or header
    :param name: The name of the parameter to get
    :param request: The request to get the parameter from, defaults to None
    :param header: The header to get the parameter from, defaults to None
    :return: The parameter, or None if it doesn't exist
    """
    d = req.args.get(name, None) if req is not None else None
    if d is None:
        d = req.headers.get(name, None)
    return d
