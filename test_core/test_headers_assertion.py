from contextlib import nullcontext as does_not_raise

from httpx import Client, Response
from httpx._models import Headers

from lib.assertion_elements.headers_assertion import _HeadersChecker

from .utils import Spec


def test_check_not_raise_when_value_is_none(mock_client: Client, mock_response: Response):
    checker = _HeadersChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(http_client=mock_client, response=mock_response, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(http_client=mock_client, response=mock_response, negative=True)


def test_check_when_header_match_response(should_not_raise: Spec, mock_client: Client, mock_response: Response):
    mock_response.headers = Headers({"SOME-HEADER": "this is the value", "OTHER": "other val"})
    checker = _HeadersChecker(value={"some-HEADER": "value"})
    with should_not_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_not_raise.negative)


def test_check_when_header_not_match_response(should_raise: Spec, mock_client: Client, mock_response: Response):
    mock_response.headers = Headers({"SOME-HEADER": "this is the value", "OTHER": "other val"})
    checker = _HeadersChecker(value={"some-HEADER": "value not match"})
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)
