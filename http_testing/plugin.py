import json
import secrets
from tempfile import NamedTemporaryFile
from typing import Any, Dict

import pytest
from httpx import URL, Client, Response
from pytest import FixtureRequest

from http_testing._assertion_elements.assert_element_checker_base import AssertElementCheckerBase
from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing.page_checker import PageChecker


@pytest.fixture
def base_url(request: FixtureRequest):
    if not hasattr(request.module, "host"):
        return None
    host = getattr(request.module, "host")
    scheme = "https" if not hasattr(request.module, "scheme") else getattr(request.module, "scheme")
    port = None if not hasattr(request.module, "port") else int(getattr(request.module, "port"))
    return URL(scheme=scheme, host=host, port=port)


@pytest.fixture
def http_client():
    with Client() as client:
        yield client


@pytest.fixture
def check(http_client: Client, base_url: URL):
    return PageChecker(http_client=http_client, base_url=base_url)


def pytest_assertrepr_compare(config, op, left, right):
    if isinstance(left, AssertionData) and isinstance(right, AssertElementCheckerBase) and op == "in":
        title = left.title or f"{left.url}-{secrets.token_hex(5)}"
        msg = ""
        if left.response:
            file_name = _dump_response(title=title, response=left.response)
            msg = f"    - please check file '{file_name}'"
        return [f"in check '{title}' - {right.assert_fail_description}", msg]
    return None


def _dump_response(title: str, response: Response) -> str:
    """
    Save the response's essential contents into a temporay file
    Return the file name
    """
    request = response.request
    result: Dict[str, Any] = {
        "title": title,
        "request": {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "content": request.content.decode(),
            "content_hex": request.content.hex(),
        },
        "response:": {
            "status_code": response.status_code,
            "content": response.text,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
        },
    }
    with NamedTemporaryFile(mode="wt", delete=False) as f:
        json.dump(obj=result, fp=f, indent=4)
        return f.name
