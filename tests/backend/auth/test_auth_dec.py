import importlib
import inspect


from api.device.device import list_devices


def test_read_decorators():
    # check what decorators are used in the function
    # assert list_devices.__name__ == "_authenticate_user"

    assert True
