from contextlib import nullcontext as does_not_raise

from httpx import Client, Response

from lib.assertion_elements.content_assertion import _ContentChecker

from .utils import Spec


def test_check_not_raise_when_value_is_none(mock_client: Client, mock_response: Response):
    checker = _ContentChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(http_client=mock_client, response=mock_response, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(http_client=mock_client, response=mock_response, negative=True)


def test_check_when_value_match_response_content(should_not_raise: Spec, mock_client: Client, mock_response: Response):
    mock_response.text = "some test \n value in response"  # type: ignore
    checker = _ContentChecker(value=["test \n value"])
    with should_not_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_not_raise.negative)


def test_check_when_value_not_match_response_content(should_raise: Spec, mock_client: Client, mock_response: Response):
    mock_response.text = "some test value in response"  # type: ignore
    checker = _ContentChecker(value=["test not existing value"])
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)
