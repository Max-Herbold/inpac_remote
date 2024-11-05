import json
import typing

import pytest

from app import app as internal_app

if typing.TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


def _decode_response(response: "bytes") -> dict:
    # decode and convert to json
    return json.loads(response.decode("utf-8"))


# pytest the /api/test endpoint
def test_ping(test_client: "FlaskClient"):
    # This test is intended to prevent deployment if the app cannot be started
    response = test_client.get("/api/test")

    # check the status code
    assert response.status_code == 200

    json_r = _decode_response(response.data)

    assert json_r["response"] == "success"


@pytest.fixture
def test_client() -> "Flask":
    return internal_app.test_client()
