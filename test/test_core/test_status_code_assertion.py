from contextlib import nullcontext as does_not_raise

from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.status_code_assertion import StatusCodeChecker

from .utils import Spec


def test_check_with_status_code_match(should_not_raise: Spec, fake_assertion_data: AssertionData):
    checker = StatusCodeChecker(value=200, negative_assertion=should_not_raise.negative)
    with should_not_raise.expected:
        assert evolve(fake_assertion_data, response_status_code=200) in checker


def test_check_with_status_code_not_match(should_raise: Spec, fake_assertion_data: AssertionData):
    checker = StatusCodeChecker(value=200, negative_assertion=should_raise.negative)
    with should_raise.expected:
        assert evolve(fake_assertion_data, response_status_code=400) in checker


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    with does_not_raise():
        # negative = False
        checker = StatusCodeChecker(value=None, negative_assertion=False)
        assert fake_assertion_data in checker

    with does_not_raise():
        # negative = True
        checker = StatusCodeChecker(value=None, negative_assertion=True)
        assert fake_assertion_data in checker
