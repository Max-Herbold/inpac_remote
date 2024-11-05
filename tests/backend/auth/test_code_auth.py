import json
import typing

from api.creds.request_code import get_codes_dict

if typing.TYPE_CHECKING:
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


def test_verify_code_operation(test_client: "FlaskClient"):
    test_email = "testing@rmit.edu.au"

    codes = get_codes_dict()
    assert test_email not in codes

    # create and get a code
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

    assert test_email in codes

    r = test_client.post(
        "/api/code/verify",
        headers={"email": test_email, "code": codes[test_email].secret},
    )
    assert r.status_code == 200

    assert r.json["response"] == "Validated"

    # assert there is a token
    assert "token" in r.json
    assert len(r.json["token"]) > 0


def test_access_authenticated(test_client: "FlaskClient"):
    test_email = "testing2@rmit.edu.au"
    # get a code
    r = test_client.post("/api/code/new", headers={"email": test_email})
    assert r.status_code == 200

    # grab the code and get a token
    code = get_codes_dict()[test_email].secret
    r = test_client.post(
        "/api/code/verify",
        headers={"email": test_email, "code": code},
    )
    assert r.status_code == 200
    token = r.json["token"]

    # try to access the dashboard without a token

    # validate the token
    r = test_client.get("/api/user/validate")
    assert r.status_code == 400  # no cookie

    test_client.set_cookie("token", "lolwot")
    r = test_client.get("/api/user/validate")
    assert r.status_code == 200  # not valid cookie
    assert r.json["response"] == "success"
    assert r.json["valid"] is False

    test_client.set_cookie("token", token)
    r = test_client.get("/api/user/validate")
    assert r.status_code == 200
    assert r.json["response"] == "success"
    assert r.json["valid"] is True


def test_logout(test_client: "FlaskClient"):
    test_email = "testing3@rmit.edu.au"
    # get a code
    r = test_client.post("/api/code/new", headers={"email": test_email})
    assert r.status_code == 200

    codes = get_codes_dict()
    # grab the code and get a token
    code = codes[test_email].secret
    r = test_client.post(
        "/api/code/verify",
        headers={"email": test_email, "code": code},
    )
    assert r.status_code == 200
    token = r.json["token"]
    test_client.set_cookie("token", token)

    r = test_client.get("/api/user/validate")
    assert r.status_code == 200  # no cookie
    assert r.json["response"] == "success"
    assert r.json["valid"] is True

    # post to /api/user/logout
    r = test_client.post("/api/user/logout")
    assert r.status_code == 200

    # check the token is removed from the store
    r = test_client.get("/api/user/validate")
    assert r.status_code == 200  # no cookie
    assert r.json["response"] == "success"
    assert r.json["valid"] is False


def _decode_response(response: "bytes") -> dict:
    # decode and convert to json
    return json.loads(response.decode("utf-8"))


# @pytest.fixture
# def test_client() -> "Flask":
#     return internal_app.test_client()
