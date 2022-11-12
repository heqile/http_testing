from http.cookiejar import Cookie as HttpCookie
from http.cookiejar import CookieJar
from unittest import mock

import pytest
from httpx import Client, Response

from lib.assertion_elements.cookies_assertion import Cookie, _CookiesChecker


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


def test_check_should_not_raise_with_same_cookie_name_on_multiple_sites():
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A())
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A_on_another_site())
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", domain="site_one")]).check(
        http_client=mock_client, response=mock_response, negative=False
    )


def test_check_should_raise_with_not_cookie_match_on_same_site():
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A_on_another_site())
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    assert_element = _CookiesChecker(
        value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", domain="site_one")]
    )
    with pytest.raises(AssertionError):
        assert_element.check(http_client=mock_client, response=mock_response, negative=False)


def test_check_should_raise_when_secure_not_match():
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A())
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    assert_element = _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", secure=True)])
    with pytest.raises(AssertionError):
        assert_element.check(http_client=mock_client, response=mock_response, negative=False)


def test_check_should_raise_when_expiration_not_match():
    mock_client = mock.MagicMock(spec=Client, auto_spec=True)
    mock_client.cookies.jar = CookieJar()
    mock_client.cookies.jar.set_cookie(CookieSuite.cookie_A())
    mock_response = mock.MagicMock(spec=Response, auto_spec=True)
    assert_element = _CookiesChecker(value=[Cookie(name="cookie_one", value_pattern="cookie_value_one", expires=1)])
    with pytest.raises(AssertionError):
        assert_element.check(http_client=mock_client, response=mock_response, negative=False)
