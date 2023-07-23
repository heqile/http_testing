from contextlib import nullcontext as does_not_raise

from httpx import Client, Response

from http_testing._assertion_elements.status_code_assertion import _StatusCodeChecker

from .utils import Spec


def test_check_with_status_code_match(should_not_raise: Spec, mock_client: Client, mock_response: Response):
    mock_response.status_code = 200
    checker = _StatusCodeChecker(value=200)
    with should_not_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_not_raise.negative)


def test_check_with_status_code_not_match(should_raise: Spec, mock_client: Client, mock_response: Response):
    mock_response.status_code = 400
    checker = _StatusCodeChecker(value=200)
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)


def test_check_not_raise_when_value_is_none(mock_client: Client, mock_response: Response):
    checker = _StatusCodeChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(http_client=mock_client, response=mock_response, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(http_client=mock_client, response=mock_response, negative=True)
