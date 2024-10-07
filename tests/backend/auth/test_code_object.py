import time

from api.creds.management.code_object import CodeObject


def test_code_object():
    code = CodeObject()
    assert code.is_expired() is False

    secret = code.secret

    assert code.validate_secret("testfalse") is False
    assert code.validate_secret(secret) is True

    assert code.is_expired() is False

    # Since the code has been validated previously
    # it should not be valid anymore
    assert code.validate_secret(secret) is False


def test_code_expired():
    code = CodeObject(_live_for_seconds=0.1)
    assert code.is_expired() is False
    time.sleep(0.2)
    assert code.is_expired() is True

    secret = code.secret

    assert code.validate_secret(secret) is False

    assert code.is_expired() is True


def test_code_attempts():
    code = CodeObject()
    assert code.is_expired() is False

    secret = code.secret

    assert code.validate_secret("test1") is False
    assert code.validate_secret("test2") is False
    assert code.validate_secret("test3") is False

    assert code.validate_secret(secret) is False
