import re
from http.cookiejar import Cookie as HttpCookie
from typing import Mapping, Optional, Sequence

from httpx import Client, Response

from ..cookie import Cookie
from .assert_element_base import AssertElementBase
from .assertion_base import AssertionBase


class _CookiesAssertElement(AssertElementBase):
    value: Optional[Sequence[Cookie]]

    def check(self, http_client: Client, response: Response, negative: bool = False) -> None:
        if self.value is None:
            return
        for cookie in self.value:
            all_cookies = {
                **{cookiejar.name: cookiejar for cookiejar in http_client.cookies.jar},
                **{cookiejar.name: cookiejar for cookiejar in response.cookies.jar},
            }
            is_cookie_exist = self._is_cookie_match(target_cookie=cookie, cookies=all_cookies)
            if (not is_cookie_exist) ^ negative:
                raise AssertionError(
                    self._make_message(
                        info=f"'{cookie.name}':'{cookie.value_pattern}'",
                        check_type="cookies",
                        url=str(response.url),
                        negative=negative,
                    )
                )

    @staticmethod
    def _is_cookie_match(target_cookie: Cookie, cookies: Mapping[str, HttpCookie]):
        cookie = cookies.get(target_cookie.name)
        if cookie is None or cookie.value is None:
            return False
        if re.search(target_cookie.value_pattern, cookie.value) is None:
            return False
        return True


class CookiesAssertion(AssertionBase):
    _assert_type = _CookiesAssertElement
