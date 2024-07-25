from contextlib import nullcontext as does_not_raise

import pytest
from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.headers_assertion import HeadersChecker
from http_testing.validators import Regex

from .utils import Spec


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    with does_not_raise():
        # negative = False
        checker = HeadersChecker(value=None, negative_assertion=False)
        assert fake_assertion_data in checker

    with does_not_raise():
        # negative = True
        checker = HeadersChecker(value=None, negative_assertion=True)
        assert fake_assertion_data in checker


@pytest.mark.parametrize(
    "response_headers, check_headers",
    [
        pytest.param(
            {"SOME-HEADER": "this is the value", "OTHER": "other val"},
            {"some-HEADER": "value"},
            id="header_match_response",
        ),
        pytest.param(
            {"SOME-HEADER": "this is the value", "OTHER": "other val"},
            {"some-HEADER": Regex(".*value$")},
            id="regex_expected_value_when_header_match_response",
        ),
    ],
)
def test_check_not_raise(should_not_raise: Spec, fake_assertion_data: AssertionData, response_headers, check_headers):
    checker = HeadersChecker(value=check_headers, negative_assertion=should_not_raise.negative)
    with should_not_raise.expected:
        assert evolve(fake_assertion_data, response_headers=response_headers) in checker


@pytest.mark.parametrize(
    "response_headers, check_headers",
    [
        pytest.param(
            {"SOME-HEADER": "this is the value", "OTHER": "other val"},
            {"some-HEADER": "value not match"},
            id="header_not_match_response",
        ),
        pytest.param(
            {"SOME-HEADER": "this is the value", "OTHER": "other val"},
            {"some-HEADER": Regex(".*not match")},
            id="regex_expected_value_when_header_not_match_response",
        ),
    ],
)
def test_check_when_header_not_match_response(
    should_raise: Spec, fake_assertion_data: AssertionData, response_headers, check_headers
):
    checker = HeadersChecker(value=check_headers, negative_assertion=should_raise.negative)
    with should_raise.expected:
        assert evolve(fake_assertion_data, response_headers=response_headers) in checker
