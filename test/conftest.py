import pytest
from httpx import URL, Client
from pytest import FixtureRequest

from lib.page_checker import PageChecker


@pytest.fixture
def http_client():
    with Client(
        trust_env=False,
        verify=False,
    ) as client:
        yield client


@pytest.fixture
def check(request: FixtureRequest, http_client: Client):
    if not hasattr(request.module, "host"):
        raise ValueError("'host' should be set in test file")
    host = getattr(request.module, "host")
    scheme = "https" if not hasattr(request.module, "scheme") else getattr(request.module, "scheme")
    port = None if not hasattr(request.module, "port") else int(getattr(request.module, "port"))
    return PageChecker(http_client=http_client, base_url=URL(scheme=scheme, host=host, port=port))
