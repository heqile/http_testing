from contextlib import nullcontext
from unittest import mock

import pytest
from httpx import Client, Response

from lib.assertion_elements.status_code_assertion import _StatusCodeChecker


@pytest.mark.parametrize(
    "negative, expected_raise",
    [
        pytest.param(
            False,
            nullcontext(),
            id="should_not_raise",
        ),
        pytest.param(
            True,
            pytest.raises(AssertionError),
            id="should_raise_when_negative_is_true",
        ),
    ],
)
def test_check_with_status_code_match(negative, expected_raise):
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    mock_response.status_code = 200
    checker = _StatusCodeChecker(value=200)
    with expected_raise:
        checker.check(http_client=mock_client, response=mock_response, negative=negative)


@pytest.mark.parametrize(
    "negative, expected_raise",
    [
        pytest.param(
            False,
            pytest.raises(AssertionError),
            id="should_raise",
        ),
        pytest.param(
            True,
            nullcontext(),
            id="should_not_raise_when_negative_is_true",
        ),
    ],
)
def test_check_with_status_code_not_match(negative, expected_raise):
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    mock_response.status_code = 400
    checker = _StatusCodeChecker(value=200)
    with expected_raise:
        checker.check(http_client=mock_client, response=mock_response, negative=negative)
