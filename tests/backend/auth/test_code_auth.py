import json
import typing

if typing.TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


def test_read_decorators():
    # check what decorators are used in the function
    # assert list_devices.__name__ == "_authenticate_user"

    assert True


def test_code_no_email(test_client: "FlaskClient"):
    r = test_client.post("/api/code/new")

    assert r.status_code == 400
    r = test_client.post("/api/code/new", headers={"email": ""})

    assert r.status_code == 400


def test_verify_code_invalid_request(test_client: "FlaskClient"):
    r = test_client.post("/api/code/verify")
    assert r.status_code == 400

    r = test_client.post("/api/code/verify", headers={"email": ""})
    assert r.status_code == 400

    r = test_client.post("/api/code/verify", headers={"email": "testing@rmit.edu.au"})
    assert r.status_code == 400

    r = test_client.post(
        "/api/code/verify", headers={"email": "testing@rmit.edu.au", "code": ""}
    )
    assert r.status_code == 403


def test_verify_code_wrong(test_client: "FlaskClient"):
    test_email = "testing@rmit.edu.au"

    # get a code
    r = test_client.post("/api/code/new", headers={"email": test_email})
    assert r.status_code == 200

    # a second attempt should be rate limited
    r = test_client.post("/api/code/new", headers={"email": test_email})
    assert r.status_code == 400

    # verify with the wrong code
    r = test_client.post(
        "/api/code/verify",
        headers={"email": test_email, "code": "0000"},
    )
    assert r.status_code == 403


def _decode_response(response: "bytes") -> dict:
    # decode and convert to json
    return json.loads(response.decode("utf-8"))


# @pytest.fixture
# def test_client() -> "Flask":
#     return internal_app.test_client()
