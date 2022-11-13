from unittest import mock

from httpx import Client, Response

from lib.assertion_elements.status_code_assertion import _StatusCodeChecker

from .utils import Spec


def test_check_with_status_code_match(should_not_raise: Spec):
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    mock_response.status_code = 200
    checker = _StatusCodeChecker(value=200)
    with should_not_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_not_raise.negative)


def test_check_with_status_code_not_match(should_raise: Spec):
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    mock_response.status_code = 400
    checker = _StatusCodeChecker(value=200)
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)
