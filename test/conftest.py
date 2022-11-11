import dataclasses

import pytest
from httpx import URL, Client
from pytest import FixtureRequest

from lib.http_client_configuration import HttpClientConfiguration
from lib.page_checker import PageChecker


@pytest.fixture
def http_client_config():
    return HttpClientConfiguration(
        trust_env=False,
        verify=False,
    )


@pytest.fixture
def http_client(http_client_config: HttpClientConfiguration):
    with Client(**dataclasses.asdict(http_client_config)) as client:
        yield client


@pytest.fixture
def check(request: FixtureRequest, http_client: Client):
    if not hasattr(request.module, "host"):
        raise ValueError("'host' should be set in test file")
    host = getattr(request.module, "host")
    scheme = "https" if not hasattr(request.module, "scheme") else getattr(request.module, "scheme")
    port = None if not hasattr(request.module, "port") else int(getattr(request.module, "port"))
    return PageChecker(http_client=http_client, base_url=URL(scheme=scheme, host=host, port=port))
