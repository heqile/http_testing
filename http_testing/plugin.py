import attrs
import pytest
from httpx import URL, Client
from pytest import FixtureRequest

from .http_client_configuration import HttpClientConfiguration
from .page_checker import PageChecker


@pytest.fixture
def base_url(request: FixtureRequest):
    if not hasattr(request.module, "host"):
        return None
    host = getattr(request.module, "host")
    scheme = "https" if not hasattr(request.module, "scheme") else getattr(request.module, "scheme")
    port = None if not hasattr(request.module, "port") else int(getattr(request.module, "port"))
    return URL(scheme=scheme, host=host, port=port)


@pytest.fixture
def http_client_config():
    return HttpClientConfiguration()


@pytest.fixture
def http_client(http_client_config: HttpClientConfiguration):
    with Client(**attrs.asdict(http_client_config)) as client:
        yield client


@pytest.fixture
def check(http_client: Client, base_url: URL):
    return PageChecker(http_client=http_client, base_url=base_url)
