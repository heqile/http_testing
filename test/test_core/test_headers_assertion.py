from contextlib import nullcontext as does_not_raise

import pytest
from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.headers_assertion import _HeadersChecker
from http_testing.validators import Regex

from .utils import Spec


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    checker = _HeadersChecker(value=None)
    with does_not_raise():
        # negative = False
        assert evolve(fake_assertion_data, negative_assertion=False) in checker

    with does_not_raise():
        # negative = True
        assert evolve(fake_assertion_data, negative_assertion=True) in checker


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
    checker = _HeadersChecker(value=check_headers)
    with should_not_raise.expected:
        assert (
            evolve(fake_assertion_data, response_headers=response_headers, negative_assertion=should_not_raise.negative)
            in checker
        )


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
    checker = _HeadersChecker(value=check_headers)
    with should_raise.expected:
        assert (
            evolve(fake_assertion_data, response_headers=response_headers, negative_assertion=should_raise.negative)
            in checker
        )
