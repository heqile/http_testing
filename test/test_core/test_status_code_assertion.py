from contextlib import nullcontext as does_not_raise

from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData
from http_testing._assertion_elements.status_code_assertion import _StatusCodeChecker

from .utils import Spec


def test_check_with_status_code_match(should_not_raise: Spec, fake_assertion_data: AssertionData):
    assertion_data = evolve(fake_assertion_data, response_status_code=200)
    checker = _StatusCodeChecker(value=200)
    with should_not_raise.expected:
        checker.check(assertion_data=assertion_data, negative=should_not_raise.negative)


def test_check_with_status_code_not_match(should_raise: Spec, fake_assertion_data: AssertionData):
    assertion_data = evolve(fake_assertion_data, response_status_code=400)
    checker = _StatusCodeChecker(value=200)
    with should_raise.expected:
        checker.check(assertion_data=assertion_data, negative=should_raise.negative)


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    checker = _StatusCodeChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(assertion_data=fake_assertion_data, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(assertion_data=fake_assertion_data, negative=True)
