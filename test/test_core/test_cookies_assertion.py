from contextlib import nullcontext as does_not_raise

import pytest
from attrs import evolve

from http_testing._assertion_elements.assertion_data import AssertionData, HttpClientCookie
from http_testing._assertion_elements.cookies_assertion import _CookiesChecker
from http_testing.cookie import Cookie
from http_testing.validators import Regex

from .utils import Spec


class CookieSuite:
    @staticmethod
    def cookie_A():
        return HttpClientCookie(
            name="cookie_one",
            value="cookie_value_one",
            domain="site_one",
            path="/",
            secure=False,
            expires=1234,
        )

    @staticmethod
    def cookie_A_on_another_site():
        return evolve(CookieSuite.cookie_A(), value="another_cookie_one", domain="site_two")

    @staticmethod
    def cookie_A_without_domain():
        return evolve(CookieSuite.cookie_A(), value="another_cookie_one", domain=None)


@pytest.mark.parametrize(
    "all_cookies, check_cookies",
    [
        pytest.param(
            {CookieSuite.cookie_A().name: [CookieSuite.cookie_A(), CookieSuite.cookie_A_on_another_site()]},
            [Cookie(name="cookie_one", value="cookie_value_one", domain="site_one")],
            id="same_cookie_name_on_multiple_sites",
        ),
        pytest.param(
            {CookieSuite.cookie_A().name: [CookieSuite.cookie_A(), CookieSuite.cookie_A_on_another_site()]},
            [Cookie(name="cookie_one", value=Regex("cookie_value_.*"), domain="site_one")],
            id="regex_value_with_same_cookie_name_on_multiple_sites",
        ),
    ],
)
def test_check_not_raise(should_not_raise: Spec, fake_assertion_data: AssertionData, all_cookies, check_cookies):
    assertion_data = evolve(fake_assertion_data, all_cookies=all_cookies)
    checker = _CookiesChecker(value=check_cookies)
    with should_not_raise.expected:
        checker.check(assertion_data=assertion_data, negative=should_not_raise.negative)


@pytest.mark.parametrize(
    "all_cookies, check_cookies",
    [
        pytest.param(
            {CookieSuite.cookie_A().name: [CookieSuite.cookie_A_on_another_site()]},
            [Cookie(name="cookie_one", value="cookie_value_one", domain="site_one")],
            id="no_cookie_match_on_same_site",
        ),
        pytest.param(
            {CookieSuite.cookie_A().name: [CookieSuite.cookie_A()]},
            [Cookie(name="cookie_one", value="cookie_value_one", secure=True)],
            id="secure_not_match",
        ),
        pytest.param(
            {CookieSuite.cookie_A().name: [CookieSuite.cookie_A()]},
            [Cookie(name="cookie_one", value="cookie_value_one", expires=1)],
            id="expiration_not_match",
        ),
    ],
)
def test_check_with_not_cookie_match_on_same_site(
    should_raise: Spec, fake_assertion_data: AssertionData, all_cookies, check_cookies
):
    assertion_data = evolve(fake_assertion_data, all_cookies=all_cookies)
    checker = _CookiesChecker(value=check_cookies)
    with should_raise.expected:
        checker.check(assertion_data=assertion_data, negative=should_raise.negative)


def test_check_not_raise_when_value_is_none(fake_assertion_data: AssertionData):
    checker = _CookiesChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(assertion_data=fake_assertion_data, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(assertion_data=fake_assertion_data, negative=True)
