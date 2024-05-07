from contextlib import nullcontext as does_not_raise

import pytest
from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.content_assertion import _ContentChecker
from http_testing.validators import Regex

from .utils import Spec


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    checker = _ContentChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(assertion_data=fake_assertion_data, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(assertion_data=fake_assertion_data, negative=True)


@pytest.mark.parametrize(
    "response_text, check_value",
    [
        pytest.param(
            "some test \n value in response",
            ["test \n value"],
            id="text_value_match_response_content_with_list_assertion_data",
        ),
        pytest.param(
            "some test \n value in response",
            [Regex(pattern="test.*\n.*value")],
            id="regex_value_match_response_content_with_list_assertion_data",
        ),
        pytest.param("some test \n value in response", "test \n value", id="text_value_match_response_content"),
        pytest.param(
            "some test \n value in response",
            Regex(pattern="test.*\n.*value"),
            id="regex_value_match_response_content",
        ),
    ],
)
def test_check_not_raise(should_not_raise: Spec, fake_assertion_data: AssertionData, response_text, check_value):
    assertion_data = evolve(fake_assertion_data, response_text=response_text)
    checker = _ContentChecker(value=check_value)
    with should_not_raise.expected:
        checker.check(assertion_data=assertion_data, negative=should_not_raise.negative)


@pytest.mark.parametrize(
    "response_text, check_value",
    [
        pytest.param(
            "some test value in response", ["test not existing value"], id="text_value_not_match_response_content"
        ),
        pytest.param(
            "some test value in response",
            [Regex(pattern="test not existing value")],
            id="regex_value_not_match_response_content",
        ),
    ],
)
def test_check_when_text_value_not_match_response_content(
    should_raise: Spec, fake_assertion_data: AssertionData, response_text, check_value
):
    assertion_data = evolve(fake_assertion_data, response_text="some test value in response")
    checker = _ContentChecker(value=["test not existing value"])
    with should_raise.expected:
        checker.check(assertion_data=assertion_data, negative=should_raise.negative)
