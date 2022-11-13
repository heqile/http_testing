from contextlib import nullcontext as does_not_raise
from http.cookiejar import Cookie as HttpCookie
from http.cookiejar import CookieJar

from httpx import Client, Response

from http_testing.assertion_elements.cookies_assertion import Cookie, _CookiesChecker

from .utils import Spec


class CookieSuite:
    @staticmethod
    def cookie_A():
        return HttpCookie(
            version=None,
            name="cookie_one",
            value="cookie_value_one",
            port=None,
            port_specified=False,
            domain="site_one",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=1234,
            discard=False,
            comment=None,
            comment_url=None,
            rest={},
            rfc2109=False,
        )

    @staticmethod
    def cookie_A_on_another_site():
        cookie = CookieSuite.cookie_A()
        cookie.value = "another_cookie_one"
        cookie.domain = "site_two"
        return cookie


def test_check_with_same_cookie_name_on_multiple_sites(
    should_not_raise: Spec, mock_client: Client, mock_response: Response
):
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A())
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A_on_another_site())
    checker = _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", domain="site_one")])
    with should_not_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_not_raise.negative)


def test_check_with_not_cookie_match_on_same_site(should_raise: Spec, mock_client: Client, mock_response: Response):
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A_on_another_site())
    checker = _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", domain="site_one")])
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)


def test_check_when_secure_not_match(should_raise: Spec, mock_client: Client, mock_response: Response):
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A())
    checker = _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", secure=True)])
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)


def test_check_should_raise_when_expiration_not_match(should_raise: Spec, mock_client: Client, mock_response: Response):
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A())
    checker = _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", expires=1)])
    with should_raise.expected:
        checker.check(http_client=mock_client, response=mock_response, negative=should_raise.negative)


def test_check_not_raise_when_value_is_none(mock_client: Client, mock_response: Response):
    checker = _CookiesChecker(value=None)
    with does_not_raise():
        # negative = False
        checker.check(http_client=mock_client, response=mock_response, negative=False)

    with does_not_raise():
        # negative = True
        checker.check(http_client=mock_client, response=mock_response, negative=True)
