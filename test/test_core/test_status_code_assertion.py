from contextlib import nullcontext as does_not_raise

from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.status_code_assertion import _StatusCodeChecker

from .utils import Spec


def test_check_with_status_code_match(should_not_raise: Spec, fake_assertion_data: AssertionData):
    checker = _StatusCodeChecker(value=200)
    with should_not_raise.expected:
        assert (
            evolve(fake_assertion_data, response_status_code=200, negative_assertion=should_not_raise.negative)
            in checker
        )


def test_check_with_status_code_not_match(should_raise: Spec, fake_assertion_data: AssertionData):
    checker = _StatusCodeChecker(value=200)
    with should_raise.expected:
        assert (
            evolve(fake_assertion_data, response_status_code=400, negative_assertion=should_raise.negative) in checker
        )


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    checker = _StatusCodeChecker(value=None)
    with does_not_raise():
        # negative = False
        assert evolve(fake_assertion_data, negative_assertion=False) in checker

    with does_not_raise():
        # negative = True
        assert evolve(fake_assertion_data, negative_assertion=True) in checker
