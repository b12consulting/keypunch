from unittest.mock import MagicMock

from pytest import fixture

from keypunch import KClient
from keypunch.client import Endpoint


@fixture(scope="function")
def kclient():
    Endpoint.form = MagicMock()
    Endpoint.post = MagicMock()
    Endpoint.put = MagicMock()
    Endpoint.get = MagicMock()

    base_url = "http://localhost:8080"
    return KClient(base_url=base_url)
