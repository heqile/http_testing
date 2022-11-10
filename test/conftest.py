import pytest
from httpx import URL
from pytest import FixtureRequest

from lib.page_checker import PageChecker


@pytest.fixture
def check(request: FixtureRequest):
    if not hasattr(request.module, "host"):
        raise ValueError("'host' should be set in test file")
    host = getattr(request.module, "host")
    scheme = "https" if not hasattr(request.module, "scheme") else getattr(request.module, "scheme")
    port = None if not hasattr(request.module, "port") else int(getattr(request.module, "port"))
    with PageChecker(base_url=URL(scheme=scheme, host=host, port=port)) as checker:
        yield checker
